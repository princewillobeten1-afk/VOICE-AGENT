from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin


class Workspace(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "workspaces"
    __table_args__ = (UniqueConstraint("organization_id", "slug", name="uq_workspace_org_slug"),)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)
    projects = relationship("Project", back_populates="workspace")


class Project(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "projects"
    __table_args__ = (UniqueConstraint("workspace_id", "slug", name="uq_project_workspace_slug"),)
    workspace_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text)
    archived_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)
    workspace = relationship("Workspace", back_populates="projects")


Index("ix_workspaces_org_active", Workspace.organization_id, Workspace.deleted_at)
Index("ix_projects_workspace_active", Project.workspace_id, Project.deleted_at)