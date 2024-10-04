import asyncio
from playwright.async_api import Playwright, ElementHandle
from typing import List, Dict, Any
import re
from utils import convert_fa_numbers
from .scraper import Scraper, ScraperException
import aiohttp
import itertools

class DigiKalaScraper(Scraper):
    def __init__(self, store_code: str, limit_count: int):
        super().__init__()
        self.store_code = store_code.upper()
        self.limit_count = limit_count

    async def __login_with_email(self, email, code):
        pass
        """
            TODO:
                implement login with email and get email code
        """

    async def __login_with_phonenumber(self, phonenumber, code):
        pass
        """
            TODO:
                implement login with phonenumber and sms code
        """

    async def __collect_goldis_products(self, url: str):
        try:
            async with self.session.get(url) as resp:
                json = await resp.json()

            products = []    
            for var in json['data']['product']['variants']:
                if var['seller']['code'].upper() == self.store_code:
                    products.append(var)
            return products
        except Exception as err:
            raise ScraperException('extract product info error', original_exception=err)

    async def __get_products_of_page(self, page_url: str) -> Any:
        try:
            async with self.session.get(page_url) as resp:
                return await resp.json()
        except Exception as err:
            raise ScraperException(f'cannot get page: {page_url}', original_exception=err)

    async def __list_all_products(self, url, page_count):

        pages, page_tasks = [], []

        for i in range(page_count):
            if (i+1) % self.limit_count == 0:
                pages.extend(await asyncio.gather(*page_tasks))
                page_tasks.clear()

            page_tasks.append(self.__get_products_of_page(f'{url}?page={i+1}'))

        if page_tasks:
            pages.extend(await asyncio.gather(*page_tasks))
            page_tasks.clear()


        counter = 1
        products, tasks = [], []
        for page in pages:
            for product in page['data']['products']:
                if counter % self.limit_count == 0:
                    products.extend(itertools.chain(*(await asyncio.gather(*tasks))))
                    tasks.clear()
                tasks.append(self.__collect_goldis_products('https://api.digikala.com/v2/product/{}/'.format(product['id'])))
                counter += 1

        if tasks:
            products.extend(await asyncio.gather(*tasks))
            tasks.clear()

        return products
                
    """
    login to digikala and return resp set-cookies
    """
    async def login(self, login_url: str, **kwargs):
        resp = None
        if kwargs.get('phonenumber'):
            resp = self.__login_with_phonenumber(kwargs['phonenumber'])
        elif kwargs.get('email'):
            resp = self.__login_with_email(kwargs.get('email'))
        else:
            raise ScraperException('login phonenumber and email not found')
        return resp.cookies

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