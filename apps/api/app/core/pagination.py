from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=25, ge=1, le=200)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


PageQuery = Annotated[int, Query(ge=1)]
PageSizeQuery = Annotated[int, Query(ge=1, le=200)]


def pagination_params(page: PageQuery = 1, page_size: PageSizeQuery = 25) -> PaginationParams:
    return PaginationParams(page=page, page_size=page_size)