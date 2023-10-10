from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.settings import db_setting

DATABASE_URL = f"postgresql+asyncpg://{db_setting.USERNAME}:{db_setting.PASSWORD}@{db_setting.HOST}:{db_setting.PORT}/{db_setting.DATABASE}"

engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
