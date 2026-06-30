from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.ai.schemas import AgentOut


class WorkspaceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    organization_id: UUID
    name: str
    slug: str
    description: str | None = None
    settings: dict
    created_at: datetime
    updated_at: datetime


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    organization_id: UUID
    workspace_id: UUID
    name: str
    slug: str
    description: str | None = None
    settings: dict
    created_at: datetime
    updated_at: datetime


class DemoBootstrapOut(BaseModel):
    workspace: WorkspaceOut
    project: ProjectOut
    agents: list[AgentOut]