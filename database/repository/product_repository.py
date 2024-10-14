from .genric_repository import Repository
from database.models.product import *
from database import get_async_session
from sqlalchemy import select
import logging

class ProductRepository(Repository):

    def __init__(self):
        super().__init__(Product)

    async def get_by_product_id(self, pid: int, store_id: int):
        async with get_async_session() as session:
            try:
                result = await session.execute(select(Product).where(Product.product_id == pid and Product.store_id == store_id))
                return result.scalar_one_or_none()
            except Exception as err:
                logging.error(f'get product by id and store_id error: {err}')

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