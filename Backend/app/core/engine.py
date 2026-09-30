from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.setting import settings

DATABASE_URL = settings.DATABASE_URL

ENGINE=create_async_engine(DATABASE_URL,poolclass=NullPool)

SESSION=async_sessionmaker(bind=ENGINE,autoflush=False,expire_on_commit=False,autocommit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with SESSION() as session:
        yield session
