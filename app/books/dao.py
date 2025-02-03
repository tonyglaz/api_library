# индивидуальные функции, относящиеся к конкретной сущности
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, selectinload
from app.dao.base import BaseDAO
from app.books.models import Book, BookGenre
from app.issue.models import BookIssue
from app.database import async_session_maker


class BookDAO(BaseDAO):
    model = Book

    @classmethod
    async def find_all_books(cls):
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(cls.model.authors), selectinload(
                cls.model.genres).selectinload(BookGenre.genre),selectinload(cls.model.issued_user))
            result = await session.execute(query)

            books = result.scalars().all()  # Получаем всех авторов
            books_data = []
            for book in books:
                print(book)
                books_dict = book.to_dict()
                print(books_dict)
                books_data.append(books_dict)
            return books_data

    @classmethod
    async def find_one_or_none_by_id(cls, book_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(
                id=book_id).options(
                    selectinload(cls.model.authors),
                    selectinload(cls.model.genres).selectinload(BookGenre.genre),
                    selectinload(cls.model.issued_user).selectinload(BookIssue.user))
            result = await session.execute(query)
            author = result.scalars().one_or_none()
            if not author:
                return None
            return author

    @classmethod
    async def add_book(cls, **book_data: dict) -> int:
        async with async_session_maker() as session:
            async with session.begin():
                new_book = Book(**book_data)
                session.add(new_book)
                await session.flush()
                # Эта операция отправляет все изменения, сделанные в текущей сессии, в базу данных, но не фиксирует транзакцию.
                # Это означает, что все изменения становятся видимыми для других операций в рамках текущей сессии, но они не будут постоянными до тех пор, пока вы не выполните commit().
                # Вызов flush() может быть полезен, если вам нужно получить идентификаторы или другие значения, которые генерируются базой данных (например, автоинкрементные ID) до выполнения commit().
                new_book_id = new_book.id
                await session.commit()
                return new_book_id

    @classmethod
    async def update_book_by_id(cls, book_id: int, **book_data) -> int:
        # Фильтруем только те поля, которые не равны None
        filtered_book_data = {k: v for k,
                              v in book_data["book_data"].items() if v is not None}
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    update(cls.model)
                    .where(cls.model.id == int(book_id))
                    .values(**filtered_book_data)
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)

            try:
                await session.commit()  # Сохраняются изменения в базе данных.
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount

    @classmethod
    async def delete_book_by_id(cls, book_id: int) -> int:
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(id=book_id)
                result = await session.execute(query)
                book_to_delete = result.scalar_one_or_none()

                if not book_to_delete:
                    return None
                await session.execute(
                    delete(cls.model).filter_by(id=book_id)
                )

                await session.commit()
                return book_id
