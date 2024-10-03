from abc import ABC, abstractmethod
import asyncio
from aiohttp import ClientSession


class ScraperException(Exception):
    def __init__(self, message, original_exception=None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)

    def __str__(self):
        if self.original_exception:
            return f"{self.message}. Original exception: {self.original_exception}"
        return self.message


class Scraper(ABC):
    def __init__(self, session: ClientSession):
        super().__init__()
        self.session = session
            
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.session.close()
        except Exception as err:
            raise ScraperException('cannot close session', original_exception=err)

    @abstractmethod
    async def decrease_product(self, **kwargs):     
        raise NotImplementedError()
    
    @abstractmethod
    async def increase_product(self, **kwargs):
        raise NotImplementedError()
    
    @abstractmethod
    async def get_product_page(self, **kwargs):
        raise NotImplementedError()
    
    @abstractmethod
    async def list_all_products(self, **kwargs):
        raise NotImplementedError()
    
    @abstractmethod
    async def login(login_url: str, **kwargs):
        raise NotImplementedError()
    
