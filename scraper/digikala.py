import asyncio
from playwright.async_api import Playwright, ElementHandle
from typing import List, Dict, Any
import re
from utils import convert_fa_numbers
from .scraper import Scraper, ScraperException
import aiohttp

class DigiKalaScraper(Scraper):
    def __init__(self):
        super().__init__()

    async def __login_with_email(self, email, code):
        pass

    async def __login_with_phonenumber(self, phonenumber, code):
        pass

    async def __get_products_of_page(self, session: aiohttp.ClientSession, page_url: str) -> Any:
        try:
            async with session.get(page_url) as resp:
                return await resp.json()
        except Exception as err:
            raise ScraperException(f'cannot get page: {page_url}', original_exception=err)

    async def __list_all_products(self, url, page_count):
        pages = None

        try:
            async with aiohttp.ClientSession() as session:
                pages = await asyncio.gather(
                   *[
                        self.__get_products_of_page(session, f'{url}?page={i+1}') 
                        for i in range(page_count)
                    ]
                )
        except Exception as err:
            raise ScraperException('cannot retrieve data from pages', original_exception=err)
        
        for page in pages:
            for product in page['data']['products']:
                yield product

    async def login(login_url: str, **kwargs):
        pass

    async def list_all_products(self, **kwargs):
        if not kwargs.get('url'):
            raise ScraperException('url not found error')
        
        page_count = 1
        if kwargs.get('page_count'):
            page_count = kwargs['page_count']

        return await self.__list_all_products(kwargs['url'], page_count)

    async def get_product_page(self, **kwargs):
        """
        TODO:
            get page of a product by it's dkp
        """
        pass

    async def increase_product(self, **kwargs):
        """
        TODO:
            increase product's quantity
        """
        pass

    async def decrease_product(self, **kwargs):
        """
        TODO:
            decrease product's quantity
        """
        pass

         