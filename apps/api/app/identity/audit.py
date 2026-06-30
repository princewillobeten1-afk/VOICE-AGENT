from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.identity.models import AuditLog


async def audit(
    db: AsyncSession,
    event_type: str,
    actor_user_id: UUID | None = None,
    organization_id: UUID | None = None,
    target_type: str | None = None,
    target_id: UUID | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    metadata: dict | None = None,
) -> None:
    db.add(
        AuditLog(
            event_type=event_type,
            actor_user_id=actor_user_id,
            organization_id=organization_id,
            target_type=target_type,
            target_id=target_id,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata_json=metadata or {},
        )
    )