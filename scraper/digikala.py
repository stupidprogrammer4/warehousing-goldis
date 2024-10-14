import asyncio
from typing import List, Dict, Any
import re
from utils import convert_fa_numbers
from .scraper import Scraper, ScraperException
import aiohttp
import aiofile
import itertools
import json
import os

class DigiKalaScraper(Scraper):
    def __init__(self, limit_count: int, cookies_path: str):
        super().__init__()
        self.limit_count = limit_count
        self.cookies_path = cookies_path
        self.base_url = 'https://seller.digikala.com/api/v2/variants'
        self.base_params = '?size=10&sort=product_variant_id&order=desc'
        

    async def __login_with_email(self, login_url, email):
        pass
        """
            TODO:
                implement login with email and verfication email code
        """

    async def __login_with_email_pass(self, login_url, email, password):
        async with self.session.post(login_url, json={
            'username': email,
            'password': password,
            'type': 'password',
            'backUrl': '/'
        }) as resp:
            return resp
        
    async def load_cookies(self):
        try:
            async with aiofile.async_open(self.cookies_path) as f:
                buffer = await f.read()
            raw_cookies = buffer.split(' ')
            cookies = {}
            for cookie in raw_cookies:
                key, val = cookie.split('=', 1)
                cookies[key] = val
            self.session.cookie_jar.update_cookies(cookies)
        except Exception as err:
            raise ScraperException('load cookies error', original_exception=err)
            

    async def __login_with_phonenumber(self, login_url, phonenumber):
        pass
        """
            TODO:
                implement login with phonenumber and sms code
        """
    async def __get_products_of_page(self, page_url: str) -> Any:
        try:
            async with self.session.get(page_url) as resp:
                return await resp.json()
        except Exception as err:
            raise ScraperException('get products of a page error', original_exception=err)

    async def __list_all_products(self, page_count):
        products, tasks = [], []
        for i in range(page_count):
            if (i+1) % self.limit_count == 0:
                responses = await asyncio.gather(*tasks)
                for resp in responses:
                    products.extend(resp['data']['items'])
                tasks.clear()

            tasks.append(self.__get_products_of_page(f'{self.base_url}{self.base_params}&page={i+1}'))

        if len(tasks):
            responses = await asyncio.gather(*tasks)
            for resp in responses:
                products.extend(resp['data']['items'])
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
            if kwargs.get('password'):
                resp = await self.__login_with_email_pass(login_url, kwargs['email'], kwargs['password'])
            else:
                resp = await self.__login_with_email(login_url, kwargs['email'])
        else:
            raise ScraperException('login phonenumber and email not found')
        return resp.cookies

    async def list_all_products(self, **kwargs):
        page_count = 1
        if kwargs.get('page_count'):
            page_count = kwargs['page_count']

        products = await self.__list_all_products(page_count)
        json_products = {}

        for product in products:
            dkp = product['product_id']
            if json_products.get(dkp) is None:
                json_products[dkp] = {'title': product['product_title'], 'variants': []}
    
            json_products[dkp]['variants'].append({
                    'id': product['id'],
                    'stock': product['marketplace_seller_stock'],
                    'size': product['gold_price_parameters']['size'] if product.get('gold_price_parameters') else 0.,
                    'price': product['price_sale'],
                    'image': product['image_src']
                })

        return json_products

    async def change_stock_of_product(self, pid, count):
        try:
            async with self.session.put(f'{self.base_url}/{pid}', json={'id': pid, 'seller_stock': count}) as resp:
                result = await resp.json()
                return result['status'] == 200
        except Exception as err:
            raise ScraperException(f'cannot update stock of product with id {pid} and count {count}', original_exception=err)
        
    async def get_products_of_page(self, page):
        return await self.__get_products_of_page(f'{self.base_url}{self.base_params}&page={page}')