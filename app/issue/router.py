from fastapi import APIRouter, Depends
from app.users.dao import UsersDAO
from app.books.dao import BookDAO
from app.issue.dao import BooksIssueDAO
from app.books.schemas import SBook, SBookADD, SBookUPD
from app.exceptions import *
from datetime import date

router = APIRouter(prefix="/issue", tags=["Работа с выдачей книг"])


@router.post("/issue-book/")
async def issue_book(book_id: int, user_id: int):
    book =  await BookDAO.find_one_or_none_by_id(book_id)
    if not book:
        raise NoBookException
    user = await UsersDAO.find_one_or_none_by_id(user_id)
    if not user:
        raise NoUserException
    # print(book.to_dict())
    # print(user.to_dict())
    # print(len(user.borrowed_books))
    if book.available_copies <= 0:
        NoBookCopiesAvailableException
    
    if len(user.borrowed_books) >=5:
        raise MaximumBooksException

    check = await BooksIssueDAO.add_issue(book_id=book_id,user_id=user_id)
    if check:
        return {"message": f"Книга  '{book.title}' успешно выдана читателю {user.first_name} {user.last_name}!"}
    else:
        return {"message": "Ошибка при выдаче книги!"}
    # Проверка, что у читателя не более 5 книг
    # user_books = # db.query(BookIssue).filter(BookIssue.user_id == user_id, BookIssue.return_date.is_(None)).count()


@router.get("/return-book-info/")
async def return_book(book_id: int, user_id: int):
    pass
    issue = await BooksIssueDAO.find_issue(book_id=book_id,user_id=user_id)
    
    if issue:
        if issue.return_date:
            return {"message": f"Книга  '{issue.book.title}' была возвращена читателем {issue.user.first_name} {issue.user.last_name} {issue.return_date} числа."}
        return {"message": f"Книга  '{issue.book.title}' была выдана читателю {issue.user.first_name} {issue.user.last_name} {issue.issue_date} числа, возврату подлежит до {issue.due_date} числа."}
    else:
        return {"message": "Не найдена книга, которую надо вернуть"}
    # issue.return_date = datetime.utcnow()

    # book = filter(Book.id == book_id)
    # if book:
    # book.available_copies += 1


@router.put("/return-book/")
async def return_book(book_id: int, user_id: int):
    issue = await BooksIssueDAO.find_issue(book_id=book_id,user_id=user_id)
    
    return_date = date.today()
    
    check = await BooksIssueDAO.return_book(issue_id=issue.id,return_date=return_date)
    if check:
        return {"message": f"Книга  '{issue.book.title}' была возвращена читателем {issue.user.first_name} {issue.user.last_name} {return_date} числа."}
    else:
        return {"message": f"Книга  '{issue.book.title}' не возвращена!"}
    
    