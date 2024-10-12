from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self, pg: AsyncSession):
        self.db = pg
