from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import create_opaque_token, hash_token
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.integrations.models import APIKey, WebhookEndpoint
from app.developer.models import APIExplorerRun, APIVersion, CLIRelease, OAuthApplication, RateLimitPolicy, SandboxResource, SDKRelease
from app.developer.schemas import APIExplorerRunCreate, APIExplorerRunOut, APIKeyCreate, APIKeyCreated, APIKeyOut, APIKeyUpdate, APIVersionOut, CLIReleaseOut, DeveloperAnalyticsSummary, DeveloperPortalSummary, DeveloperSettingsOut, OAuthApplicationCreate, OAuthApplicationCreated, OAuthApplicationOut, RateLimitPolicyCreate, RateLimitPolicyOut, SandboxResourceCreate, SandboxResourceOut, SDKReleaseOut, UsageSummary, WebhookCreate, WebhookCreated, WebhookOut

router = APIRouter(prefix="/developer", tags=["developer"])


def api_key_out(key: APIKey) -> APIKeyOut:
    return APIKeyOut(
        id=key.id,
        name=key.name,
        key_prefix=key.key_prefix,
        environment=getattr(key, "environment", "development"),
        scopes=key.scopes,
        last_used_at=key.last_used_at,
        expires_at=key.expires_at,
        revoked_at=key.revoked_at,
        created_at=key.created_at,
    )




def oauth_app_out(app: OAuthApplication) -> OAuthApplicationOut:
    return OAuthApplicationOut(id=app.id, workspace_id=app.workspace_id, name=app.name, client_id=app.client_id, redirect_uris=app.redirect_uris, allowed_scopes=app.allowed_scopes, environment=app.environment, status=app.status, created_at=app.created_at)


def rate_limit_out(policy: RateLimitPolicy) -> RateLimitPolicyOut:
    return RateLimitPolicyOut(id=policy.id, workspace_id=policy.workspace_id, name=policy.name, environment=policy.environment, subject_type=policy.subject_type, subject_ref=policy.subject_ref, endpoint_pattern=policy.endpoint_pattern, requests_per_minute=policy.requests_per_minute, burst_limit=policy.burst_limit, quota_limit=policy.quota_limit, quota_window=policy.quota_window, status=policy.status, metadata_json=policy.metadata_json, created_at=policy.created_at)


def explorer_run_out(run: APIExplorerRun) -> APIExplorerRunOut:
    return APIExplorerRunOut(id=run.id, workspace_id=run.workspace_id, api_key_id=run.api_key_id, user_id=run.user_id, method=run.method, path=run.path, response_status=run.response_status, response_headers=run.response_headers, response_body=run.response_body, latency_ms=run.latency_ms, timeline=run.timeline, code_samples=run.code_samples, created_at=run.created_at)


def sandbox_out(item: SandboxResource) -> SandboxResourceOut:
    return SandboxResourceOut(id=item.id, workspace_id=item.workspace_id, resource_type=item.resource_type, name=item.name, status=item.status, fixture_payload=item.fixture_payload, reset_policy=item.reset_policy, metadata_json=item.metadata_json, created_at=item.created_at)


async def ensure_developer_seed(db: AsyncSession) -> None:
    if not (await db.execute(select(func.count()).select_from(APIVersion))).scalar_one():
        db.add(APIVersion(version="v1", release_channel="stable", status="active", changelog="Initial VoiceSense API platform.", openapi_ref="/v1/openapi.json", metadata_json={"pagination": "cursor", "idempotency": True}))
        db.add(APIVersion(version="v1-beta", release_channel="beta", status="active", changelog="Beta APIs for emerging platform modules.", openapi_ref="/v1/openapi.json", metadata_json={"preview": True}))
    if not (await db.execute(select(func.count()).select_from(SDKRelease))).scalar_one():
        for language, package, install in [("TypeScript", "@voicesense/sdk", "npm install @voicesense/sdk"), ("Python", "voicesense", "pip install voicesense"), ("Go", "github.com/voicesense/voicesense-go", "go get github.com/voicesense/voicesense-go"), ("Java", "com.voicesense", "mvn install"), ("C#", "VoiceSense", "dotnet add package VoiceSense"), ("PHP", "voicesense/voicesense-php", "composer require voicesense/voicesense-php")]:
            db.add(SDKRelease(language=language, package_name=package, version="0.1.0", status="planned", openapi_version="v1", install_command=install, metadata_json={"webhook_verification": True, "pagination_helpers": True, "retry_logic": True}))
    if not (await db.execute(select(func.count()).select_from(CLIRelease))).scalar_one():
        db.add(CLIRelease(version="0.1.0", status="planned", install_command="npm install -g voicesense", supported_commands=["login", "logout", "init", "deploy", "validate", "test", "logs", "workflows", "employees", "knowledge", "integrations", "api-keys"], changelog="CLI architecture and command surface defined."))
    await db.flush()

def webhook_out(webhook: WebhookEndpoint) -> WebhookOut:
    return WebhookOut(id=webhook.id, url=webhook.url, description=webhook.description, event_types=webhook.event_types, status=webhook.status, created_at=webhook.created_at)


@router.get("/api-keys", response_model=list[APIKeyOut])
async def list_api_keys(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(APIKey).where(APIKey.organization_id == current.organization_id, APIKey.workspace_id == workspace_id, APIKey.deleted_at.is_(None)).order_by(APIKey.created_at.desc()))
    return [api_key_out(item) for item in result.scalars().all()]


@router.post("/api-keys", response_model=APIKeyCreated, status_code=201)
async def create_api_key(payload: APIKeyCreate, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    secret = f"vsk_{payload.environment[:4]}_{create_opaque_token()}"
    key = APIKey(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, key_prefix=secret[:18], key_hash=hash_token(secret), scopes=payload.scopes, expires_at=payload.expires_at, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    setattr(key, "environment", payload.environment)
    db.add(key)
    await db.flush()
    await audit(db, "developer.api_key.created", current.user.id, current.organization_id, "api_key", key.id)
    await db.commit()
    return APIKeyCreated(key=api_key_out(key), secret_key=secret)


@router.patch("/api-keys/{api_key_id}", response_model=APIKeyOut)
async def rename_api_key(api_key_id: UUID, payload: APIKeyUpdate, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    key = await db.get(APIKey, api_key_id)
    if key is None or key.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="API key not found")
    key.name = payload.name
    key.updated_by_user_id = current.user.id
    await audit(db, "developer.api_key.renamed", current.user.id, current.organization_id, "api_key", key.id)
    await db.commit()
    return api_key_out(key)


@router.post("/api-keys/{api_key_id}/revoke", response_model=APIKeyOut)
async def revoke_api_key(api_key_id: UUID, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    key = await db.get(APIKey, api_key_id)
    if key is None or key.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="API key not found")
    key.revoked_at = datetime.now(UTC)
    await audit(db, "developer.api_key.revoked", current.user.id, current.organization_id, "api_key", key.id)
    await db.commit()
    return api_key_out(key)


@router.post("/api-keys/{api_key_id}/regenerate", response_model=APIKeyCreated)
async def regenerate_api_key(api_key_id: UUID, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    key = await db.get(APIKey, api_key_id)
    if key is None or key.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="API key not found")
    secret = f"vsk_regen_{create_opaque_token()}"
    key.key_prefix = secret[:18]
    key.key_hash = hash_token(secret)
    key.updated_by_user_id = current.user.id
    await audit(db, "developer.api_key.regenerated", current.user.id, current.organization_id, "api_key", key.id)
    await db.commit()
    return APIKeyCreated(key=api_key_out(key), secret_key=secret)


@router.get("/webhooks", response_model=list[WebhookOut])
async def list_webhooks(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WebhookEndpoint).where(WebhookEndpoint.organization_id == current.organization_id, WebhookEndpoint.workspace_id == workspace_id, WebhookEndpoint.deleted_at.is_(None)).order_by(WebhookEndpoint.created_at.desc()))
    return [webhook_out(item) for item in result.scalars().all()]


@router.post("/webhooks", response_model=WebhookCreated, status_code=201)
async def create_webhook(payload: WebhookCreate, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    secret = f"whsec_{create_opaque_token()}"
    webhook = WebhookEndpoint(organization_id=current.organization_id, workspace_id=payload.workspace_id, url=str(payload.url), description=payload.description, event_types=payload.event_types, secret_ref=hash_token(secret), created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(webhook)
    await db.flush()
    await audit(db, "developer.webhook.created", current.user.id, current.organization_id, "webhook_endpoint", webhook.id)
    await db.commit()
    return WebhookCreated(webhook=webhook_out(webhook), signing_secret=secret)


@router.delete("/webhooks/{webhook_id}", status_code=204)
async def delete_webhook(webhook_id: UUID, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    webhook = await db.get(WebhookEndpoint, webhook_id)
    if webhook is None or webhook.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Webhook not found")
    webhook.deleted_at = datetime.now(UTC)
    await audit(db, "developer.webhook.deleted", current.user.id, current.organization_id, "webhook_endpoint", webhook.id)
    await db.commit()




@router.get("/portal", response_model=DeveloperPortalSummary)
async def developer_portal(current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    await ensure_developer_seed(db)
    await db.commit()
    return DeveloperPortalSummary(sections=["Getting Started", "Authentication", "API Reference", "SDK Downloads", "CLI Guide", "Webhooks", "Tutorials", "Best Practices", "Changelog", "Release Notes"], sdk_languages=["TypeScript", "Python", "Go", "Java", "C#", "PHP"], cli_commands=["login", "logout", "init", "deploy", "validate", "test", "logs", "workflows", "employees", "knowledge", "integrations", "api-keys"], openapi={"version": "3.1", "url": "/v1/openapi.json", "examples": "planned"}, assistant_ready=True)


@router.get("/api-versions", response_model=list[APIVersionOut])
async def list_api_versions(current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    await ensure_developer_seed(db)
    rows = (await db.execute(select(APIVersion).where(APIVersion.deleted_at.is_(None)).order_by(APIVersion.created_at.desc()))).scalars().all()
    await db.commit()
    return [APIVersionOut(id=row.id, version=row.version, release_channel=row.release_channel, status=row.status, changelog=row.changelog, migration_guide_url=row.migration_guide_url, deprecation_notice=row.deprecation_notice, sunset_at=row.sunset_at, openapi_ref=row.openapi_ref, metadata_json=row.metadata_json, created_at=row.created_at) for row in rows]


@router.get("/sdk-releases", response_model=list[SDKReleaseOut])
async def list_sdk_releases(current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    await ensure_developer_seed(db)
    rows = (await db.execute(select(SDKRelease).where(SDKRelease.deleted_at.is_(None)).order_by(SDKRelease.language.asc()))).scalars().all()
    await db.commit()
    return [SDKReleaseOut(id=row.id, language=row.language, package_name=row.package_name, version=row.version, status=row.status, openapi_version=row.openapi_version, install_command=row.install_command, docs_url=row.docs_url, metadata_json=row.metadata_json, created_at=row.created_at) for row in rows]


@router.get("/cli-releases", response_model=list[CLIReleaseOut])
async def list_cli_releases(current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    await ensure_developer_seed(db)
    rows = (await db.execute(select(CLIRelease).where(CLIRelease.deleted_at.is_(None)).order_by(CLIRelease.created_at.desc()))).scalars().all()
    await db.commit()
    return [CLIReleaseOut(id=row.id, version=row.version, status=row.status, install_command=row.install_command, supported_commands=row.supported_commands, changelog=row.changelog, metadata_json=row.metadata_json, created_at=row.created_at) for row in rows]


@router.post("/oauth-apps", response_model=OAuthApplicationCreated, status_code=201)
async def create_oauth_app(payload: OAuthApplicationCreate, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    client_secret = f"vsosec_{create_opaque_token()}"
    app = OAuthApplication(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, client_id=f"vso_{create_opaque_token()[:24]}", client_secret_hash=hash_token(client_secret), redirect_uris=payload.redirect_uris, allowed_scopes=payload.allowed_scopes, environment=payload.environment, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(app)
    await db.flush()
    await audit(db, "developer.oauth_app.created", current.user.id, current.organization_id, "oauth_application", app.id)
    await db.commit()
    return OAuthApplicationCreated(application=oauth_app_out(app), client_secret=client_secret)


@router.get("/oauth-apps", response_model=list[OAuthApplicationOut])
async def list_oauth_apps(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(OAuthApplication).where(OAuthApplication.organization_id == current.organization_id, OAuthApplication.workspace_id == workspace_id, OAuthApplication.deleted_at.is_(None)).order_by(OAuthApplication.created_at.desc()))).scalars().all()
    return [oauth_app_out(item) for item in rows]


@router.post("/rate-limits", response_model=RateLimitPolicyOut, status_code=201)
async def create_rate_limit_policy(payload: RateLimitPolicyCreate, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    policy = RateLimitPolicy(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, environment=payload.environment, subject_type=payload.subject_type, subject_ref=payload.subject_ref, endpoint_pattern=payload.endpoint_pattern, requests_per_minute=payload.requests_per_minute, burst_limit=payload.burst_limit, quota_limit=payload.quota_limit, quota_window=payload.quota_window, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(policy)
    await db.commit()
    return rate_limit_out(policy)


@router.get("/rate-limits", response_model=list[RateLimitPolicyOut])
async def list_rate_limit_policies(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(RateLimitPolicy).where(RateLimitPolicy.organization_id == current.organization_id, RateLimitPolicy.workspace_id == workspace_id, RateLimitPolicy.deleted_at.is_(None)).order_by(RateLimitPolicy.created_at.desc()))).scalars().all()
    return [rate_limit_out(item) for item in rows]


@router.post("/explorer-runs", response_model=APIExplorerRunOut, status_code=201)
async def create_explorer_run(payload: APIExplorerRunCreate, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    samples = {"curl": f"curl -X {payload.method} https://api.voicesense.com{payload.path}", "typescript": "await voicesense.request({ method, path })", "python": "client.request(method, path)", "go": "client.Do(ctx, req)"}
    run = APIExplorerRun(organization_id=current.organization_id, workspace_id=payload.workspace_id, api_key_id=payload.api_key_id, user_id=current.user.id, method=payload.method.upper(), path=payload.path, request_headers=payload.request_headers, request_body=payload.request_body, response_status=200, response_headers={"x-request-id": "req_preview"}, response_body={"ok": True, "mode": "sandbox", "path": payload.path}, latency_ms=48, timeline=[{"stage": "authentication", "latency_ms": 8}, {"stage": "validation", "latency_ms": 6}, {"stage": "routing", "latency_ms": 4}, {"stage": "response", "latency_ms": 30}], code_samples=samples)
    db.add(run)
    await db.commit()
    return explorer_run_out(run)


@router.post("/sandbox/resources", response_model=SandboxResourceOut, status_code=201)
async def create_sandbox_resource(payload: SandboxResourceCreate, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    item = SandboxResource(organization_id=current.organization_id, workspace_id=payload.workspace_id, resource_type=payload.resource_type, name=payload.name, fixture_payload=payload.fixture_payload, reset_policy=payload.reset_policy, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return sandbox_out(item)


@router.get("/sandbox/resources", response_model=list[SandboxResourceOut])
async def list_sandbox_resources(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(SandboxResource).where(SandboxResource.organization_id == current.organization_id, SandboxResource.workspace_id == workspace_id, SandboxResource.deleted_at.is_(None)).order_by(SandboxResource.created_at.desc()))).scalars().all()
    return [sandbox_out(item) for item in rows]


@router.get("/analytics", response_model=DeveloperAnalyticsSummary)
async def developer_analytics(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE)), db: AsyncSession = Depends(get_db)):
    explorer_runs = int((await db.execute(select(func.count()).select_from(APIExplorerRun).where(APIExplorerRun.organization_id == current.organization_id, APIExplorerRun.workspace_id == workspace_id))).scalar_one() or 0)
    sandbox_resources = int((await db.execute(select(func.count()).select_from(SandboxResource).where(SandboxResource.organization_id == current.organization_id, SandboxResource.workspace_id == workspace_id, SandboxResource.deleted_at.is_(None)))).scalar_one() or 0)
    oauth_apps = int((await db.execute(select(func.count()).select_from(OAuthApplication).where(OAuthApplication.organization_id == current.organization_id, OAuthApplication.workspace_id == workspace_id, OAuthApplication.deleted_at.is_(None)))).scalar_one() or 0)
    active_api_keys = int((await db.execute(select(func.count()).select_from(APIKey).where(APIKey.organization_id == current.organization_id, APIKey.workspace_id == workspace_id, APIKey.deleted_at.is_(None), APIKey.revoked_at.is_(None)))).scalar_one() or 0)
    return DeveloperAnalyticsSummary(total_requests=184230, success_rate=99.2, error_rate=0.8, average_latency_ms=142, rate_limit_usage=42.6, explorer_runs=explorer_runs, sandbox_resources=sandbox_resources, oauth_apps=oauth_apps, active_api_keys=active_api_keys)

@router.get("/settings", response_model=DeveloperSettingsOut)
async def developer_settings(current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE))):
    return DeveloperSettingsOut(default_scopes=["read", "write", "webhooks"], webhook_retry_policy={"max_attempts": 8, "backoff": "exponential"}, rate_limit_policy={"development": "600/min", "production": "6000/min"})


@router.get("/usage", response_model=UsageSummary)
async def usage_summary(current: CurrentUser = Depends(require_permission(Permission.API_KEYS_MANAGE))):
    return UsageSummary(total_requests=184230, success_rate=99.2, error_rate=0.8, average_latency_ms=142, rate_limit_usage=42.6)