from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.responses import APIErrorEnvelope, ErrorDetail


class VoiceSenseError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "business_error"

    def __init__(self, message: str, code: str | None = None, status_code: int | None = None):
        self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code
        super().__init__(message)


class NotFoundError(VoiceSenseError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"


class ConflictError(VoiceSenseError):
    status_code = status.HTTP_409_CONFLICT
    code = "conflict"


class PermissionDeniedError(VoiceSenseError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "permission_denied"


def request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


def error_response(request: Request, status_code: int, code: str, message: str, field: str | None = None) -> JSONResponse:
    payload = APIErrorEnvelope(error=ErrorDetail(code=code, message=message, field=field), request_id=request_id(request))
    return JSONResponse(status_code=status_code, content=payload.model_dump())


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(VoiceSenseError)
    async def voicesense_error_handler(request: Request, exc: VoiceSenseError):
        return error_response(request, exc.status_code, exc.code, exc.message)

    @app.exception_handler(HTTPException)
    async def http_error_handler(request: Request, exc: HTTPException):
        message = str(exc.detail) if exc.detail else "HTTP error"
        return error_response(request, exc.status_code, "http_error", message)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        first = exc.errors()[0] if exc.errors() else {}
        field = ".".join(str(part) for part in first.get("loc", []) if part != "body") or None
        message = first.get("msg", "Invalid request")
        return error_response(request, status.HTTP_422_UNPROCESSABLE_ENTITY, "validation_error", message, field)