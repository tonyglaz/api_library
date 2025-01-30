from app.dao.base import BaseDAO
from app.users.models import User
from app.books.models import Book
from app.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update

# переделать под книги

# @event.listens_for(Item, 'after_insert')
# def receive_after_insert(mapper, connection, target):
#     country_id = target.country_id
#     connection.execute(
#         update(Country)
#         .where(Country.id == country_id)
#         .values(count_items=Country.count_items+1)
#     )


# @event.listens_for(Item, 'after_delete')
# def receive_after_insert(mapper, connection, target):
#     country_id = target.country_id
#     connection.execute(
#         update(Country)
#         .where(Country.id == country_id)
#         .values(count_items=Country.count_items-1)
#     )


class BooksDAO(BaseDAO):
    model = User
