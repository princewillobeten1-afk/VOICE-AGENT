from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.errors import install_error_handlers
from app.core.logging import RequestLoggingMiddleware, configure_logging
from app.identity.router import router as identity_router
from app.ai.router import router as ai_router
from app.integrations.router import router as integrations_router
from app.notifications.router import events_router, router as notifications_router
from app.storage.router import router as storage_router
from app.voice.router import router as voice_router
from app.conversations.router import router as conversations_router
from app.memory.router import router as memory_router
from app.knowledge.router import router as knowledge_router
from app.retrieval.router import router as retrieval_router
from app.workflow.router import router as workflow_router
from app.tools.router import router as tools_router
from app.collaboration.router import router as collaboration_router
from app.analytics.router import router as analytics_router
from app.telephony.router import router as telephony_router
from app.omnichannel.router import router as omnichannel_router
from app.developer.router import router as developer_router
from app.billing.router import router as billing_router
from app.security.router import router as security_router
from app.aistudio.router import router as aistudio_router
from app.workspace.router import router as workspace_router
from app.live.router import router as live_router
from app.middleware.security import InMemoryRateLimitMiddleware, SecurityHeadersMiddleware

settings = get_settings()
configure_logging()

app = FastAPI(title=settings.app_name, version="0.1.0", openapi_url=f"{settings.api_prefix}/openapi.json")
install_error_handlers(app)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(InMemoryRateLimitMiddleware, limit=120, window_seconds=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.allowed_origins] or ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(identity_router, prefix=settings.api_prefix, tags=["identity"])
app.include_router(notifications_router, prefix=settings.api_prefix)
app.include_router(events_router, prefix=settings.api_prefix)
app.include_router(developer_router, prefix=settings.api_prefix)
app.include_router(billing_router, prefix=settings.api_prefix)
app.include_router(security_router, prefix=settings.api_prefix)
app.include_router(aistudio_router, prefix=settings.api_prefix)
app.include_router(workspace_router, prefix=settings.api_prefix)
app.include_router(live_router, prefix=settings.api_prefix)
app.include_router(storage_router, prefix=settings.api_prefix)
app.include_router(integrations_router, prefix=settings.api_prefix)
app.include_router(ai_router, prefix=settings.api_prefix)
app.include_router(voice_router, prefix=settings.api_prefix)
app.include_router(conversations_router, prefix=settings.api_prefix)
app.include_router(memory_router, prefix=settings.api_prefix)
app.include_router(knowledge_router, prefix=settings.api_prefix)
app.include_router(retrieval_router, prefix=settings.api_prefix)
app.include_router(workflow_router, prefix=settings.api_prefix)
app.include_router(tools_router, prefix=settings.api_prefix)
app.include_router(collaboration_router, prefix=settings.api_prefix)
app.include_router(analytics_router, prefix=settings.api_prefix)
app.include_router(telephony_router, prefix=settings.api_prefix)
app.include_router(omnichannel_router, prefix=settings.api_prefix)


@app.get("/health")
async def health():
    return {"ok": True, "service": "voicesense-api"}





