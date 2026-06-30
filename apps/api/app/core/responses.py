from typing import Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str
    field: str | None = None


class APIEnvelope(BaseModel, Generic[T]):
    ok: bool = True
    data: T | None = None
    message: str | None = None
    request_id: str | None = None


class APIErrorEnvelope(BaseModel):
    ok: bool = False
    error: ErrorDetail
    request_id: str | None = None


class PageMeta(BaseModel):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    total: int = Field(ge=0)
    has_next: bool


class Page(BaseModel, Generic[T]):
    items: list[T]
    meta: PageMeta