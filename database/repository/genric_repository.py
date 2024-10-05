from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from database import get_async_session, AsyncSessionLocal
from sqlalchemy import select
import logging
        

class IRepository(ABC):
    
    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError()
    
    @abstractmethod
    async def remove(self, id: int):
        raise NotImplementedError()
    
    @abstractmethod
    async def update(self, id: int, **fields):
        raise NotImplementedError()
    
    @abstractmethod
    async def get(self, id: int):
        raise NotImplementedError()
    
    @abstractmethod
    async def list_all(self):
        raise NotImplementedError()
    
    @abstractmethod
    async def list_by_count(self, count):
        raise NotImplementedError()
    
class Repository(IRepository):
    def __init__(self, model_cls):
        super().__init__()
        self.model_cls = model_cls

    async def create(self, *args, **kwargs):
        async with get_async_session() as session:
            try:
                model_obj = self.model_cls(*args, **kwargs)
                session.add(model_obj)
            except Exception as err:
                logging.error(f'error create {self.model_cls}. error: {err}')


    async def get(self, id: int):
        async with get_async_session() as session:
            try:
                return await session.get(self.model_cls, id)
            except Exception as err:
                logging.error(f'error get {self.model_cls} by id: {id}. error: {err}')
        
    async def update(self, id: int, **fields):
        async with get_async_session() as session:
            try:
                model_obj = await session.get(self.model_cls, id)
                for key, val in fields.items():
                    model_obj.__setattr__(key, val)
            except Exception as err:
                logging.error(f'error update {self.model_cls} with id: {id}. error: {err}')

    
    async def remove(self, id: int):
        async with get_async_session() as session:
            try:
                model_obj = await session.get(self.model_cls, id)
                await session.delete(model_obj)
            except Exception as err:
                logging.error(f'error remove from db in class {self.model_cls}. error: {err}')
    
    async def list_all(self):
        async with get_async_session() as session:
            try:
                result = await session.execute(select(self.model_cls))
                return result.scalars().all()
            except Exception as err:
                logging.error(f'error list all in class {self.model_cls}. error: {err}')
        
    async def list_by_count(self, count):
        async with get_async_session() as session:
            try:
                result = await session.execute(select(self.model_cls).limit(count))
                return result.scalars().all()
            except Exception as err:
                logging.error(f'list by count in class {self.model_cls}. error: {err}')