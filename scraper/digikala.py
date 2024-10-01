import asyncio
from playwright.async_api import Playwright, ElementHandle
from typing import List, Dict
import re
from utils import convert_fa_numbers
from .scraper import Scraper, ScraperException


class DigiKalaScraper(Scraper):
    def __init__(self, playwright: Playwright, browser_type: str, proxies=None):
        super().__init__(playwright, browser_type, proxies=proxies)

    async def __login(self, phonenumber: str, password: str, login_url: str):
        try:
            page = await self.context.new_page()

            await page.goto(login_url)
        
            username_inp = await page.query_selector('input[name="username"]')
            await username_inp.fill(phonenumber)
            btn = page.locator('div:text("ورود")')
            await btn.click()
        
            await page.wait_for_timeout(1000)
            btn = await page.query_selector('div:text("ورود با رمز عبور")')
        
            if btn:
                await btn.click()
        
            password_inp = await page.wait_for_selector('input[name="password"]')
            if password_inp:
                await password_inp.fill(password)
            btn = page.locator('div:text("تایید")')
            await btn.click()
        
            await page.wait_for_timeout(500)
            await page.close()
        except Exception as err:
            raise ScraperException('login error', original_exception=err)
        
    async def __get_products_of_page(self, url: str, page_number: int) -> List[ElementHandle]:
        try:
            page = await self.context.new_page()
            await page.goto(f'{url}/?page={page_number}')
            await page.wait_for_timeout(2000)
            divs = await page.query_selector_all('.product-list_ProductList__item__LiiNI')
            return divs
        except Exception as err:
            raise ScraperException('get products of page error', original_exception=err)
        
    async def __extract_existence(self, ele: ElementHandle):
        try:
            exist_ele = await ele.query_selector('span:not([class]):not([data-testid])')
            return exist_ele is None
        except Exception as err:
            raise ScraperException('extract check existence of product error', original_exception=err)
    
    async def __extract_title(self, ele: ElementHandle):
        try:
            title_ele = await ele.query_selector('h3')
            return await title_ele.inner_text()
        except Exception as err:
            raise ScraperException('extract title error', original_exception=err)
    
    async def __extract_dkp(self, ele: ElementHandle) -> str:
        try:
            link_ele = await ele.query_selector('a')
            href = await link_ele.get_attribute('href')
            return re.search(r'dkp-[0-9]+', href).group()
        except Exception as err:
            raise ScraperException('extract dkp error', original_exception=err)
    
    async def __extract_discount(self, ele: ElementHandle) -> int:
        try:
            discount_ele = await ele.query_selector('span[data-testid="price-discount-percent"]')
            if not discount_ele:
                return 0
            discount = await discount_ele.inner_text()
            discount_value = re.search(r'\d+', discount).group()
            return convert_fa_numbers(discount_value)
        except Exception as err:
            raise ScraperException('extract discount error', original_exception=err)
    
    async def __extract_score(self, ele: ElementHandle) -> float:
        try:
            score_ele = await ele.query_selector('p[class="text-body2-strong text-neutral-700"]')
            if not score_ele:
                return 0.
            score = await score_ele.inner_text()
            return float(score)
        except Exception as err:
            raise ScraperException('extract score exception', original_exception=err)
    
    async def __list_all_products_rotate_proxy(self, url: str, page_count):
        """
        TODO:
            using proxies for 429 error code to get more than limit count pages async
        """
        pass
    
    async def __list_products_with_limit(self, url: str, page_count: int, limit: int) -> List[Dict]:

        try:
            result: List[List[ElementHandle]] = []

            for i in range(0, page_count, limit):
                if i + limit > page_count:
                    break
                result.extend(await asyncio.gather(*[self.__get_products_of_page(url, i+j+1) for j in range(limit)]))

            st_page = limit * (page_count//limit)

            result.extend(await asyncio.gather(*[self.__get_products_of_page(url, j+1) for j in range(st_page, page_count)]))
        except Exception as err:
            raise ScraperException('gathering data from pages error', original_exception=err)

        divs: List[ElementHandle] = []
        for items in result:
            for div in items:
                divs.append(div)
        products: List[Dict] = []
        for div in divs:
            title = await self.__extract_title(div)
            is_exist = await self.__extract_existence(div)
            dkp = await self.__extract_dkp(div)
            discount = await self.__extract_discount(div)
            score = await self.__extract_score(div)
            products.append({'dkp': dkp, 'title': title, 'is_exist': is_exist, 'discount': discount, 'score': score})
        return products  
            

    async def login(self, login_url: str, **kwargs):
        if not kwargs.get('phonenumber'):
            raise ScraperException('key phonenumber not found')
        if not kwargs.get('password'):
            raise ScraperException('key password not found')
    
        return await self.__login(kwargs['phonenumber'], 
                                    kwargs['password'], login_url)
    

    async def list_all_products(self, **kwargs):
        if not kwargs.get('url'):
            raise ScraperException('key url not found')
        page_count = 1
        if kwargs.get('page_count'):
            page_count = kwargs['page_count']

        limit = page_count+1
        if kwargs.get('limit'):
            limit = kwargs['limit']

        return await self.__list_products_with_limit(kwargs['url'], page_count, limit)
    
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

         