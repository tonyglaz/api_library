from fastapi import APIRouter, Depends
from app.users.dao import UsersDAO
from app.books.dao import BookDAO
from app.books.schemas import SBook, SBookADD, SBookUPD
from app.exceptions import *

router = APIRouter(prefix="/issue", tags=["Работа с выдачей книг"])


@router.post("/issue-book/")
async def issue_book(book_id: int, user_id: int):
    book = BookDAO.find_one_or_none_by_id(book_id)
    if not book:
        NoBookException
    user = UsersDAO.find_one_or_none_by_id(user_id)
    if not user:
        NoUserException

    if book.available_copies <= 0:
        NoBookCopiesAvailableException

    # Проверка, что у читателя не более 5 книг
    # user_books = # db.query(BookIssue).filter(BookIssue.user_id == user_id, BookIssue.return_date.is_(None)).count()


@router.post("/return-book/")
async def return_book(book_id: int, user_id: int):
    pass
    # issue = BookIssueDAO.....

    # issue.return_date = datetime.utcnow()

    # book = filter(Book.id == book_id)
    # if book:
    # book.available_copies += 1
