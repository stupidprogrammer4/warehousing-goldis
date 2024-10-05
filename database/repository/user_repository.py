from .genric_repository import Repository
from database.models.user import User
from database import get_async_session
from sqlalchemy import select
import logging

class UserRepository(Repository):

    def __init__(self):
        super().__init__(User)
    
    async def get_by_username(self, username: str) -> User:
        async with get_async_session() as session:
            try:
                result = await session.execute(select(User).where(User.username == username))
                return result.scalar_one_or_none()
            except Exception as err:
                logging.error('get user by username error: %s' % err)
