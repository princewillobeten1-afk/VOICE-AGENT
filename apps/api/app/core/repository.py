from typing import Generic, TypeVar
from uuid import UUID
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT")


class Repository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, db: AsyncSession):
        self.db = db

    def base_query(self) -> Select[tuple[ModelT]]:
        return select(self.model)

    async def get(self, entity_id: UUID) -> ModelT | None:
        return await self.db.get(self.model, entity_id)

    def add(self, entity: ModelT) -> ModelT:
        self.db.add(entity)
        return entity