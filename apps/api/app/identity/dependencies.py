from dataclasses import dataclass
from uuid import UUID
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_access_token
from app.identity.models import Membership, Role, Session, User
from app.identity.rbac import Permission, role_has_permission


@dataclass(frozen=True)
class CurrentUser:
    user: User
    session: Session
    organization_id: UUID | None


async def get_current_user(authorization: str | None = Header(default=None), db: AsyncSession = Depends(get_db)) -> CurrentUser:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    try:
        payload = decode_access_token(authorization.split(" ", 1)[1])
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    user_id = UUID(payload["sub"])
    session_id = UUID(payload["sid"])
    user = (await db.execute(select(User).where(User.id == user_id, User.deleted_at.is_(None)))).scalar_one_or_none()
    session = (await db.execute(select(Session).where(Session.id == session_id, Session.user_id == user_id, Session.revoked_at.is_(None)))).scalar_one_or_none()
    if user is None or session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session is no longer active")
    org = payload.get("org")
    return CurrentUser(user=user, session=session, organization_id=UUID(org) if org else None)


def require_permission(permission: Permission):
    async def dependency(current: CurrentUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> CurrentUser:
        if current.organization_id is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No active organization")
        result = await db.execute(select(Membership, Role).join(Role, Membership.role_id == Role.id).where(Membership.user_id == current.user.id, Membership.organization_id == current.organization_id, Membership.status == "active"))
        row = result.first()
        if row is None or not role_has_permission(row[1].slug, permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current
    return dependency