from app.dao.base import BaseDAO
from app.issue.models import BookIssue
from app.books.models import Book, BookGenre
from app.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update, event
from sqlalchemy.orm import selectinload

# переделать под книги


@event.listens_for(BookIssue, 'after_insert')
def receive_after_insert(mapper, connection, target):
    book_id = target.book_id
    print(target.book_id)
    connection.execute(
        update(Book)
        .where(Book.id == book_id)
        .values(available_copies=Book.available_copies - 1)
    )


@event.listens_for(BookIssue, 'after_update')
def receive_after_update(mapper, connection, target):
    print('update started')
    if target.return_date is not None:
        book_id = target.book_id
        print(target.book_id)
        connection.execute(
            update(Book)
            .where(Book.id == book_id)
            .values(available_copies=Book.available_copies + 1)
        )


class BooksIssueDAO(BaseDAO):
    model = BookIssue

    @classmethod
    async def add_issue(cls, user_id: int, book_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                new_book_issue = BookIssue(book_id=book_id, user_id=user_id)
                session.add(new_book_issue)
                await session.flush()
                new_book_issue_id = new_book_issue.id
                await session.commit()
                return new_book_issue_id

    @classmethod
    async def find_issue(cls, user_id: int, book_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(
                    user_id=user_id, book_id=book_id).options(selectinload(cls.model.user), selectinload(
                        cls.model.book))
            result = await session.execute(query)
            book_issue = result.scalars().first()
            # print(book_issue.to_dict())
            return book_issue

    @classmethod
    async def return_book(cls, issue_id, return_date):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    update(cls.model)
                    .where(cls.model.id == int(issue_id))
                    .values(return_date=return_date)
                    .execution_options(synchronize_session="False")
                )
                result = await session.execute(query)

            try:
                await session.commit()  # Сохраняются изменения в базе данных.
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount
