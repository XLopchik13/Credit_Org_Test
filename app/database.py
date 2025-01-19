from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


DATABASE_URL = settings.database_url

async_engine = create_async_engine(
    url=DATABASE_URL,
    echo=True
)

async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False
)


async def get_db():
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
