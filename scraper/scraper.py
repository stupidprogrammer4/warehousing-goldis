from playwright.async_api import Playwright
from abc import ABC, abstractmethod
import asyncio


class ScraperException(Exception):
    def __init__(self, message, original_exception=None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)


class Scraper(ABC):
    def __init__(self, playwright: Playwright, browser_type: str, proxies=None):
        super().__init__()
        self.proxies = proxies
        match browser_type:
            case 'firefox':
                self.btype = playwright.firefox
            case 'chromium':
                self.btype = playwright.chromium
            case 'webkit':
                self.btype = playwright.webkit
            case _:
                raise ScraperException('browser type not exist')
            
    async def __aenter__(self):
        self.browser = await self.btype.launch(headless=False)
        self.context = await self.browser.new_context()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.context.close()
        await self.browser.close()

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
    
