from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
)
from config import settings


class DataBaseHelper:

    def __init__(
        self,
        db_host=settings.DB_HOST,
        db_port=settings.DB_PORT,
        db_user=settings.DB_USER,
        db_pass=settings.DB_PASS,
        db_name=settings.DB_NAME,
        echo=settings.database.echo,
        pool_size=settings.database.pool_size,
        max_overflow=settings.database.max_overflow,
    ):
        self.url = (
            f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )
        self.engine: AsyncEngine = create_async_engine(
            url=self.url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self):
        async with self.session_factory() as session:
            yield session


db_helper = DataBaseHelper()

test_db_helper = DataBaseHelper(
    db_name="project_e_test",
    db_host="test_db",
)
