# индивидуальные функции, относящиеся к конкретной сущности
from sqlalchemy.future import select
from app.dao.base import BaseDAO
from app.authors.models import Author
from app.database import async_session_maker


class AuthorDAO(BaseDAO):
    model = Author

    @classmethod
    async def update_author_by_id(cls, author_id: int):
        pass

    @classmethod
    async def add_author(cls, **author_data: dict):
        pass

    @classmethod
    async def delete_author_by_id(cls, author_id: int):
        pass
