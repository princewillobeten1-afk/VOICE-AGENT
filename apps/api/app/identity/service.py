from datetime import UTC, datetime, timedelta
from re import sub
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.core.security import create_access_token, create_opaque_token, hash_password, hash_token, verify_password
from app.identity.audit import audit
from app.identity.models import Membership, Organization, Role, Session, User, VerificationToken
from app.identity.rbac import ROLE_PERMISSIONS, RoleSlug
from app.identity.schemas import AuthResponse, AuthTokens


def normalize_email(email: str) -> str:
    return email.strip().lower()


def slugify(value: str) -> str:
    slug = sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "workspace"


async def ensure_default_roles(db: AsyncSession) -> dict[str, Role]:
    roles: dict[str, Role] = {}
    for slug, permissions in ROLE_PERMISSIONS.items():
        result = await db.execute(select(Role).where(Role.slug == slug.value))
        role = result.scalar_one_or_none()
        if role is None:
            role = Role(slug=slug.value, name=slug.value.title(), permissions=[item.value for item in permissions])
            db.add(role)
            await db.flush()
        roles[slug.value] = role
    return roles


async def create_session(db: AsyncSession, user: User, organization_id: UUID | None, user_agent: str | None, ip_address: str | None) -> tuple[Session, AuthTokens]:
    settings = get_settings()
    refresh_token = create_opaque_token()
    expires_at = datetime.now(UTC) + timedelta(days=settings.refresh_token_days)
    session = Session(user_id=user.id, refresh_token_hash=hash_token(refresh_token), user_agent=user_agent, ip_address=ip_address, expires_at=expires_at)
    db.add(session)
    await db.flush()
    access_token = create_access_token(user.id, organization_id, session.id)
    return session, AuthTokens(access_token=access_token, refresh_token=refresh_token, expires_in=settings.access_token_minutes * 60)


async def sign_up(db: AsyncSession, name: str, email: str, password: str, organization_name: str, user_agent: str | None, ip_address: str | None) -> AuthResponse:
    email_normalized = normalize_email(email)
    existing = await db.execute(select(User).where(User.email_normalized == email_normalized, User.deleted_at.is_(None)))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

    roles = await ensure_default_roles(db)
    user = User(name=name, display_name=name, email=email, email_normalized=email_normalized, password_hash=hash_password(password))
    org = Organization(name=organization_name, slug=slugify(organization_name))
    db.add_all([user, org])
    await db.flush()
    db.add(Membership(organization_id=org.id, user_id=user.id, role_id=roles[RoleSlug.OWNER.value].id))
    verification_token = create_opaque_token()
    db.add(VerificationToken(user_id=user.id, purpose="email_verification", token_hash=hash_token(verification_token), expires_at=datetime.now(UTC) + timedelta(hours=get_settings().email_verification_hours)))
    session, tokens = await create_session(db, user, org.id, user_agent, ip_address)
    await audit(db, "auth.signup", user.id, org.id, "session", session.id, ip_address, user_agent)
    await db.commit()
    return AuthResponse(user=user, organization=org, tokens=tokens)


async def sign_in(db: AsyncSession, email: str, password: str, user_agent: str | None, ip_address: str | None) -> AuthResponse:
    result = await db.execute(select(User).where(User.email_normalized == normalize_email(email), User.deleted_at.is_(None)))
    user = result.scalar_one_or_none()
    if user is None or user.password_hash is None or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if user.disabled_at is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled")

    membership_result = await db.execute(select(Membership).where(Membership.user_id == user.id, Membership.status == "active"))
    membership = membership_result.scalar_one_or_none()
    org_id = membership.organization_id if membership else None
    org = None
    if org_id:
        org = (await db.execute(select(Organization).where(Organization.id == org_id))).scalar_one_or_none()
    session, tokens = await create_session(db, user, org_id, user_agent, ip_address)
    await audit(db, "auth.signin", user.id, org_id, "session", session.id, ip_address, user_agent)
    await db.commit()
    return AuthResponse(user=user, organization=org, tokens=tokens)


async def create_verification_token(db: AsyncSession, user: User, purpose: str, minutes: int) -> str:
    token = create_opaque_token()
    db.add(VerificationToken(user_id=user.id, purpose=purpose, token_hash=hash_token(token), expires_at=datetime.now(UTC) + timedelta(minutes=minutes)))
    return token


async def revoke_session(db: AsyncSession, session_id: UUID, user_id: UUID) -> None:
    result = await db.execute(select(Session).where(Session.id == session_id, Session.user_id == user_id, Session.revoked_at.is_(None)))
    session = result.scalar_one_or_none()
    if session:
        session.revoked_at = datetime.now(UTC)
        await audit(db, "auth.session.revoked", user_id, target_type="session", target_id=session.id)
        await db.commit()