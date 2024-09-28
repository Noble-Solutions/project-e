from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload


class BaseService:
    def __init__(self, pg: AsyncSession):
        self.db = pg
