# индивидуальные функции, относящиеся к конкретной сущности
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.exc import SQLAlchemyError
from app.dao.base import BaseDAO
from app.authors.models import Author
from app.database import async_session_maker


class AuthorDAO(BaseDAO):
    model = Author

    @classmethod
    async def add_author(cls, **author_data: dict) -> int:
        async with async_session_maker() as session:
            async with session.begin():
                new_author = Author(**author_data)
                session.add(new_author)
                await session.flush()
                # Эта операция отправляет все изменения, сделанные в текущей сессии, в базу данных, но не фиксирует транзакцию.
                # Это означает, что все изменения становятся видимыми для других операций в рамках текущей сессии, но они не будут постоянными до тех пор, пока вы не выполните commit().
                # Вызов flush() может быть полезен, если вам нужно получить идентификаторы или другие значения, которые генерируются базой данных (например, автоинкрементные ID) до выполнения commit().
                new_author_id = new_author.id
                await session.commit()
                return new_author_id

    @classmethod
    async def update_author_by_id(cls,author_id:int,**author_data) -> int:
        # Фильтруем только те поля, которые не равны None
        filtered_author_data = {k: v for k, v in author_data.items() if v is not None}
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                         update(cls.model)
                         .where(cls.model.id ==int(author_id))
                         .values(**filtered_author_data)
                         .execution_options(synchronize_session="fetch")
                         )
                result = await session.execute(query)

            try:
                await session.commit()# Сохраняются изменения в базе данных.
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount

    @classmethod
    async def delete_author_by_id(cls, author_id: int) -> int:
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(id=author_id)
                result = await session.execute(query)
                author_to_delete = result.scalar_one_or_none()

                if not author_to_delete:
                    return None
                await session.execute(
                    delete(cls.model).filter_by(id=author_id)
                )

                await session.commit()
                return author_id
