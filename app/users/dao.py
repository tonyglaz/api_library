from app.dao.base import BaseDAO
from app.users.models import User
from app.issue.models import BookIssue
from app.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy import update


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def find_one_or_none(cls, user_id: int) -> User:
        async with async_session_maker() as session:
            query = select(User).filter(User.id == user_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_by_email(cls, email: str) -> User:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(email = email)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_by_id(cls, user_id: int) -> User:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id = user_id).options(selectinload(cls.model.borrowed_books).selectinload(BookIssue.book))
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def upd_to_admin(cls, user_id: int, admin: bool):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == int(user_id))
                .values(is_admin=admin, is_user=not admin)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            try:
                await session.commit()  # Сохраняются изменения в базе данных.
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount
