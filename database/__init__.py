from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import DB_NAME, DB_PASSWORD, DB_USERNAME, DB_POOL_SIZE, DB_HOST, DB_PORT
from database.models.base_model import Base
from contextlib import asynccontextmanager
from sqlalchemy.exc import SQLAlchemyError
import logging

async_engine = create_async_engine(
    f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    pool_size=DB_POOL_SIZE,
    future=True,
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def db_init():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_async_session():
    async_session = AsyncSessionLocal()
    try:
        yield async_session
        await async_session.commit()
    except SQLAlchemyError as err:
        logging.error(err)
        await async_session.rollback()
    finally:
        await async_session.close()