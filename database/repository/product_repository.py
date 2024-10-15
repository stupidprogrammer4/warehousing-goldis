from .genric_repository import Repository
from database.models.product import *
from database import get_async_session, AsyncSession
from sqlalchemy import select
import logging

class ProductRepository(Repository):

    def __init__(self):
        super().__init__(Product)

    async def __get_product_by_product_store_id(self, session: AsyncSession, 
                                                product_id: int, store_id: int):
            try:
                product = await session.execute(select(Product).where(Product.product_id == product_id and 
                                                                Product.store_id == store_id))
                return product.scalar_one_or_none()
            except Exception as err:
                logging.error(f'get product by product and store id error: {err}')
            

    async def get_by_product_id(self, product_id: int, store_id: int):
        async with get_async_session() as session:
            return await self.__get_product_by_product_store_id(session=session, 
                                                          product_id=product_id, 
                                                          store_id=store_id)

    async def add_booster(self, product_id: int, booster_id: int):
        async with get_async_session() as session:
            try:
                session.add(Booster(pid_to_boost=product_id, pid_booster=booster_id))
            except Exception as err:
                logging.error(f'add booster for product error: {err}')

    async def get_boosters(self, product_id: int, store_id: int):
        async with get_async_session() as session:
            try:
                product = await self.__get_product_by_product_store_id(session=session, 
                                                                       product_id=product_id,
                                                                       store_id=store_id)
                return await product.awaitable_attrs.boosters
            except Exception as err:
                logging.error(f'get boosters of product error: {err}')

    async def get_to_boost_products(self, product_id: int, store_id: int):
        async with get_async_session() as session:
            try:
                product = await self.__get_product_by_product_store_id(session=session,
                                                                       product_id=product_id,
                                                                       store_id=store_id)
                return await product.awaitable_attrs.to_boost_products
            except Exception as err:
                logging.error(f'get to boost products error: {err}')
            

class StoreRepository(Repository):
    def __init__(self):
        super().__init__(Store)

    async def get_by_title(self, title: str):
        async with get_async_session() as session:
            try:
                result = await session.execute(select(Store).where(Store.title == title))
                return result.scalar_one_or_none()
            except Exception as err:
                logging.error(f'get store by title error: {err}')