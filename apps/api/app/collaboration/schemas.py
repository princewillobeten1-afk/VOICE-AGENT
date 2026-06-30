from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class TeamCreate(BaseModel):
    workspace_id: UUID
    parent_team_id: UUID | None = None
    supervisor_agent_id: UUID | None = None
    name: str
    slug: str
    department: str | None = None
    description: str | None = None
    responsibilities: list[str] = Field(default_factory=list)
    routing_policy: dict = Field(default_factory=dict)
    collaboration_rules: dict = Field(default_factory=dict)
    metadata_json: dict = Field(default_factory=dict)


class TeamOut(BaseModel):
    id: UUID
    workspace_id: UUID
    parent_team_id: UUID | None
    supervisor_agent_id: UUID | None
    name: str
    slug: str
    department: str | None
    description: str | None
    responsibilities: list[str]
    routing_policy: dict
    collaboration_rules: dict
    status: str
    metadata_json: dict
    created_at: datetime
    updated_at: datetime


class MemberAssign(BaseModel):
    workspace_id: UUID
    agent_id: UUID
    role_id: UUID | None = None
    membership_type: str = "member"
    responsibilities: list[str] = Field(default_factory=list)
    availability_state: dict = Field(default_factory=dict)
    workload_score: int = 0


class MemberOut(BaseModel):
    id: UUID
    team_id: UUID
    agent_id: UUID
    role_id: UUID | None
    membership_type: str
    responsibilities: list[str]
    availability_state: dict
    workload_score: int
    status: str
    created_at: datetime


class PolicyCreate(BaseModel):
    workspace_id: UUID
    team_id: UUID | None = None
    name: str
    policy_type: str = "delegation"
    max_delegation_depth: int = 4
    allowed_delegations: dict = Field(default_factory=dict)
    approval_requirements: dict = Field(default_factory=dict)
    escalation_rules: dict = Field(default_factory=dict)
    department_restrictions: dict = Field(default_factory=dict)


class DelegationRequest(BaseModel):
    workspace_id: UUID
    session_id: UUID | None = None
    team_id: UUID | None = None
    source_agent_id: UUID | None = None
    supervisor_agent_id: UUID | None = None
    required_role: str | None = None
    task_title: str
    objective: str | None = None
    message: str | None = None
    task_payload: dict = Field(default_factory=dict)
    shared_state: dict = Field(default_factory=dict)
    success_criteria: dict = Field(default_factory=dict)
    priority: str = "normal"
    depth: int = 0
    due_at: datetime | None = None


class DelegationOut(BaseModel):
    id: UUID
    session_id: UUID | None
    source_agent_id: UUID | None
    target_agent_id: UUID | None
    team_id: UUID | None
    task_title: str
    task_payload: dict
    routing_reason: str | None
    confidence_score: float | None
    depth: int
    status: str
    due_at: datetime | None
    completed_at: datetime | None
    created_at: datetime


class SessionOut(BaseModel):
    id: UUID
    team_id: UUID | None
    conversation_id: UUID | None
    workflow_run_id: UUID | None
    supervisor_agent_id: UUID | None
    objective: str
    status: str
    priority: str
    shared_state: dict
    success_criteria: dict
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime


class LogOut(BaseModel):
    id: UUID
    session_id: UUID | None
    event_type: str
    actor_agent_id: UUID | None
    level: str
    message: str | None
    payload: dict
    created_at: datetime


class AnalyticsOut(BaseModel):
    teams: int
    members: int
    sessions: int
    active_sessions: int
    delegations: int
    success_rate: str
    average_resolution_time: str
    routing_strategy: str
