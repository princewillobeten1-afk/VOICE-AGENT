from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class APIResponse(BaseModel):
    ok: bool = True
    message: str | None = None


class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    display_name: str | None = None
    email: EmailStr
    avatar_url: str | None = None
    timezone: str = "UTC"
    language: str = "en"
    email_verified_at: datetime | None = None
    profile_settings: dict = Field(default_factory=dict)


class OrganizationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    slug: str


class TeamOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    organization_id: UUID
    name: str
    slug: str


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_agent: str | None = None
    ip_address: str | None = None
    created_at: datetime
    expires_at: datetime
    revoked_at: datetime | None = None


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthResponse(BaseModel):
    user: UserProfile
    organization: OrganizationOut | None = None
    tokens: AuthTokens


class SignUpRequest(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    email: EmailStr
    password: str = Field(min_length=12, max_length=256)
    organization_name: str = Field(min_length=2, max_length=180)


class SignInRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=256)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=32)
    password: str = Field(min_length=12, max_length=256)


class VerifyEmailRequest(BaseModel):
    token: str = Field(min_length=32)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=12, max_length=256)


class UpdateEmailRequest(BaseModel):
    email: EmailStr


class UpdateProfileRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    display_name: str | None = Field(default=None, max_length=160)
    avatar_url: str | None = None
    timezone: str | None = Field(default=None, max_length=80)
    language: str | None = Field(default=None, max_length=16)
    profile_settings: dict | None = None


class CreateOrganizationRequest(BaseModel):
    name: str = Field(min_length=2, max_length=180)


class RenameOrganizationRequest(BaseModel):
    name: str = Field(min_length=2, max_length=180)


class CreateTeamRequest(BaseModel):
    name: str = Field(min_length=2, max_length=160)


class InviteRequest(BaseModel):
    email: EmailStr
    role: str = "member"
    team_id: UUID | None = None