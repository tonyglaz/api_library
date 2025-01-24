# универсальные методы
from sqlalchemy.future import select
from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            authors = await session.execute(query)
            return authors.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, author_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=author_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        pass

    @classmethod
    # условия фильтрации и значения для обновления
    async def update(cls, filter_by, **values):
        pass

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        pass
