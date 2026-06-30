import asyncio
import json
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import func, select
from app.ai.models import Agent
from app.core.database import AsyncSessionLocal
from app.core.security import decode_access_token

router = APIRouter(prefix="/live", tags=["live"])


def sse(payload: dict) -> str:
    return f"data: {json.dumps(payload, default=str)}\n\n"


@router.get("/workspace-stream")
async def workspace_stream(access_token: str = Query(min_length=12), workspace_id: UUID | None = None):
    try:
        payload = decode_access_token(access_token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid stream token") from exc
    organization_id = UUID(payload["org"])

    async def events():
        sequence = 0
        while True:
            async with AsyncSessionLocal() as db:
                query = select(func.count()).select_from(Agent).where(Agent.organization_id == organization_id, Agent.deleted_at.is_(None))
                if workspace_id:
                    query = query.where(Agent.workspace_id == workspace_id)
                live = int((await db.execute(query.where(Agent.status == "published"))).scalar_one() or 0)
                testing = int((await db.execute(query.where(Agent.status == "testing"))).scalar_one() or 0)
                total = int((await db.execute(query)).scalar_one() or 0)
            yield sse({"type": "workspace.summary", "sequence": sequence, "total_agents": total, "live_agents": live, "testing_agents": testing})
            sequence += 1
            await asyncio.sleep(5)

    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})