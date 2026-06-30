from time import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        response.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        return response


class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 120, window_seconds: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window_seconds = window_seconds
        self.hits: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next):
        key = request.client.host if request.client else "unknown"
        now = time()
        recent = [hit for hit in self.hits.get(key, []) if now - hit < self.window_seconds]
        if len(recent) >= self.limit:
            return Response("{\"error\":{\"code\":\"rate_limited\",\"message\":\"Rate limit exceeded. Please retry shortly.\"}}", status_code=429, media_type="application/json")
        recent.append(now)
        self.hits[key] = recent
        return await call_next(request)