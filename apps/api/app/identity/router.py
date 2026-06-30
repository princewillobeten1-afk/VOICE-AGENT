from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import hash_password, hash_token, verify_password
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, get_current_user, require_permission
from app.identity.models import Invitation, Membership, Organization, Role, Session, Team, TeamMember, User, VerificationToken
from app.identity.rbac import Permission
from app.identity.schemas import *
from app.identity.service import create_verification_token, ensure_default_roles, revoke_session, sign_in, sign_up, slugify

router = APIRouter()


def request_meta(request: Request) -> tuple[str | None, str | None]:
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None
    return user_agent, ip_address


@router.post("/auth/signup", response_model=AuthResponse, status_code=201)
async def signup(payload: SignUpRequest, request: Request, db: AsyncSession = Depends(get_db)):
    user_agent, ip_address = request_meta(request)
    return await sign_up(db, payload.name, payload.email, payload.password, payload.organization_name, user_agent, ip_address)


@router.post("/auth/signin", response_model=AuthResponse)
async def signin(payload: SignInRequest, request: Request, db: AsyncSession = Depends(get_db)):
    user_agent, ip_address = request_meta(request)
    return await sign_in(db, payload.email, payload.password, user_agent, ip_address)


@router.post("/auth/signout", response_model=APIResponse)
async def signout(current: CurrentUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await revoke_session(db, current.session.id, current.user.id)
    return APIResponse(message="Signed out")


@router.post("/auth/forgot-password", response_model=APIResponse)
async def forgot_password(payload: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email_normalized == payload.email.lower(), User.deleted_at.is_(None)))).scalar_one_or_none()
    if user:
        await create_verification_token(db, user, "password_reset", get_settings().password_reset_minutes)
        await audit(db, "auth.password_reset.requested", user.id)
        await db.commit()
    return APIResponse(message="If the email exists, reset instructions will be sent")


@router.post("/auth/reset-password", response_model=APIResponse)
async def reset_password(payload: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    token = (await db.execute(select(VerificationToken).where(VerificationToken.token_hash == hash_token(payload.token), VerificationToken.purpose == "password_reset", VerificationToken.used_at.is_(None)))).scalar_one_or_none()
    if token is None or token.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    user = (await db.execute(select(User).where(User.id == token.user_id))).scalar_one()
    user.password_hash = hash_password(payload.password)
    token.used_at = datetime.now(UTC)
    await audit(db, "auth.password_reset.completed", user.id)
    await db.commit()
    return APIResponse(message="Password reset")


@router.post("/auth/verify-email", response_model=APIResponse)
async def verify_email(payload: VerifyEmailRequest, db: AsyncSession = Depends(get_db)):
    token = (await db.execute(select(VerificationToken).where(VerificationToken.token_hash == hash_token(payload.token), VerificationToken.purpose == "email_verification", VerificationToken.used_at.is_(None)))).scalar_one_or_none()
    if token is None or token.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    user = (await db.execute(select(User).where(User.id == token.user_id))).scalar_one()
    user.email_verified_at = datetime.now(UTC)
    token.used_at = datetime.now(UTC)
    await audit(db, "auth.email.verified", user.id)
    await db.commit()
    return APIResponse(message="Email verified")


@router.post("/auth/change-password", response_model=APIResponse)
async def change_password(payload: ChangePasswordRequest, current: CurrentUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current.user.password_hash is None or not verify_password(payload.current_password, current.user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current.user.password_hash = hash_password(payload.new_password)
    await audit(db, "auth.password.changed", current.user.id, current.organization_id)
    await db.commit()
    return APIResponse(message="Password changed")


@router.post("/auth/update-email", response_model=APIResponse)
async def update_email(payload: UpdateEmailRequest, current: CurrentUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    current.user.email = payload.email
    current.user.email_normalized = payload.email.lower()
    current.user.email_verified_at = None
    await create_verification_token(db, current.user, "email_verification", get_settings().email_verification_hours * 60)
    await audit(db, "auth.email.updated", current.user.id, current.organization_id)
    await db.commit()
    return APIResponse(message="Email updated; verification required")


@router.delete("/auth/account", response_model=APIResponse)
async def delete_account(current: CurrentUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    current.user.deleted_at = datetime.now(UTC)
    await audit(db, "auth.account.deleted", current.user.id, current.organization_id)
    await db.commit()
    return APIResponse(message="Account deleted")


@router.get("/users/me", response_model=UserProfile)
async def me(current: CurrentUser = Depends(get_current_user)):
    return current.user


@router.patch("/users/me", response_model=UserProfile)
async def update_me(payload: UpdateProfileRequest, current: CurrentUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(current.user, field, value)
    await audit(db, "user.profile.updated", current.user.id, current.organization_id)
    await db.commit()
    return current.user


@router.get("/sessions", response_model=list[SessionOut])
async def sessions(current: CurrentUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return (await db.execute(select(Session).where(Session.user_id == current.user.id).order_by(Session.created_at.desc()))).scalars().all()


@router.delete("/sessions/{session_id}", response_model=APIResponse)
async def delete_session(session_id: UUID, current: CurrentUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await revoke_session(db, session_id, current.user.id)
    return APIResponse(message="Session revoked")


@router.post("/organizations", response_model=OrganizationOut, status_code=201)
async def create_organization(payload: CreateOrganizationRequest, current: CurrentUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    roles = await ensure_default_roles(db)
    org = Organization(name=payload.name, slug=slugify(payload.name))
    db.add(org)
    await db.flush()
    db.add(Membership(organization_id=org.id, user_id=current.user.id, role_id=roles["owner"].id))
    await audit(db, "organization.created", current.user.id, org.id, "organization", org.id)
    await db.commit()
    return org


@router.get("/organizations", response_model=list[OrganizationOut])
async def list_organizations(current: CurrentUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Organization).join(Membership).where(Membership.user_id == current.user.id, Organization.deleted_at.is_(None)))
    return result.scalars().all()


@router.patch("/organizations/{organization_id}", response_model=OrganizationOut)
async def rename_organization(organization_id: UUID, payload: RenameOrganizationRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    org = (await db.execute(select(Organization).where(Organization.id == organization_id))).scalar_one_or_none()
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    org.name = payload.name
    await audit(db, "organization.renamed", current.user.id, org.id, "organization", org.id)
    await db.commit()
    return org


@router.delete("/organizations/{organization_id}", response_model=APIResponse)
async def delete_organization(organization_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_DELETE)), db: AsyncSession = Depends(get_db)):
    org = (await db.execute(select(Organization).where(Organization.id == organization_id))).scalar_one_or_none()
    if org:
        org.deleted_at = datetime.now(UTC)
        await audit(db, "organization.deleted", current.user.id, org.id, "organization", org.id)
        await db.commit()
    return APIResponse(message="Organization deleted")


@router.post("/organizations/{organization_id}/teams", response_model=TeamOut, status_code=201)
async def create_team(organization_id: UUID, payload: CreateTeamRequest, current: CurrentUser = Depends(require_permission(Permission.TEAM_WRITE)), db: AsyncSession = Depends(get_db)):
    team = Team(organization_id=organization_id, name=payload.name, slug=slugify(payload.name))
    db.add(team)
    await audit(db, "team.created", current.user.id, organization_id, "team", team.id)
    await db.commit()
    return team


@router.get("/organizations/{organization_id}/teams", response_model=list[TeamOut])
async def list_teams(organization_id: UUID, current: CurrentUser = Depends(require_permission(Permission.TEAM_READ)), db: AsyncSession = Depends(get_db)):
    return (await db.execute(select(Team).where(Team.organization_id == organization_id, Team.deleted_at.is_(None)))).scalars().all()


@router.post("/organizations/{organization_id}/invitations", response_model=APIResponse, status_code=201)
async def invite_member(organization_id: UUID, payload: InviteRequest, current: CurrentUser = Depends(require_permission(Permission.INVITE_CREATE)), db: AsyncSession = Depends(get_db)):
    roles = await ensure_default_roles(db)
    role = roles.get(payload.role)
    if role is None:
        raise HTTPException(status_code=400, detail="Unknown role")
    token = hash_token(payload.email + str(datetime.now(UTC).timestamp()))
    db.add(Invitation(organization_id=organization_id, team_id=payload.team_id, email=payload.email.lower(), role_id=role.id, token_hash=token, invited_by_user_id=current.user.id, expires_at=datetime.now(UTC)))
    await audit(db, "invitation.created", current.user.id, organization_id, "invitation")
    await db.commit()
    return APIResponse(message="Invitation created")