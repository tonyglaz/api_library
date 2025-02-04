from fastapi import APIRouter, Depends
from app.books.dao import BookDAO
from app.books.schemas import SBook, SBookADD, SBookUPD
from app.issue.dao import BooksIssueDAO
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.dao import UsersDAO
from app.exceptions import *
from datetime import date

router = APIRouter(prefix="/issue", tags=["Работа с выдачей книг"])


@router.post("/issue-book/")
async def issue_book(book_id: int, current_user: User = Depends(get_current_user)):
    book = await BookDAO.find_one_or_none_by_id(book_id)
    if not book:
        raise NoBookException
    if book.available_copies <= 0:
        NoBookCopiesAvailableException
    issues = await BooksIssueDAO.find_all_issues_for_one_user(user_id=current_user.id)
    if sum(1 for issue in issues if not issue.return_date) >= 5:
        raise MaximumBooksException

    check = await BooksIssueDAO.add_issue(book_id=book_id, user_id=current_user.id)
    if check:
        return {"message": f"Книга  '{book.title}' успешно выдана читателю {current_user.first_name} {current_user.last_name}!"}
    else:
        return {"message": "Ошибка при выдаче книги!"}


@router.get("/history-issues/")
async def return_book(current_user: User = Depends(get_current_user)):
    issues = await BooksIssueDAO.find_all_issues_for_one_user(user_id=current_user.id)
    response = []
    for issue in issues:
        if issue.return_date:
            response.append({"message": f"Книга  '{issue.book.title}' была возвращена читателем {issue.user.first_name} {issue.user.last_name} {issue.return_date} числа."})
        else:
            response.append( {"message": f"Книга  '{issue.book.title}' была выдана читателю {issue.user.first_name} {issue.user.last_name} {issue.issue_date} числа, возврату подлежит до {issue.due_date} числа."})
    if response:
        return response
    else:
        return {"message": "Запись о выдаче книги не найдена!"}


@router.put("/return-book/")
async def return_book(book_id: int, current_user: User = Depends(get_current_user)):
    issue = await BooksIssueDAO.find_issue(book_id=book_id, user_id=current_user.id)
    return_date = date.today()

    if issue:
        check = await BooksIssueDAO.return_book(issue_id=issue.id, return_date=return_date)
    else:
        return {"message": "Запись о выдаче книги не найдена! (Возможно книга уже была возвращена)"}

    if check:
        return {"message": f"Книга  '{issue.book.title}' была возвращена читателем {issue.user.first_name} {issue.user.last_name} {return_date} числа."}
    else:
        return {"message": f"Книга  '{issue.book.title}' не возвращена!"}
