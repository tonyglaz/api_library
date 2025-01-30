from fastapi import APIRouter
from app.books.dao import BookDAO
from app.books.schemas import SBook, SBookADD, SBookUPD

router = APIRouter(prefix="/books", tags=["Работа с книгами"])


@router.get("/", summary="Получить все книги")
async def get_all_books():
    return await BookDAO.find_all_books()


@router.get("/{id}/", summary="Получить одну книгу по ID")
async def get_book_by_id(book_id: int):
    result = await BookDAO.find_one_or_none_by_id(book_id)
    if result is None:
        return {"message": f"Книга с ID {book_id} не найдена!"}
    return result


@router.post("/add/")
async def add_book(book: SBookADD) -> dict:
    check = await BookDAO.add_book(**book.model_dump())
    if check:
        return {"message": "Книга успешно добавлена!", "book": book}
    else:
        return {"message": "Ошибка при добавлении книги!"}


@router.put("/upd/{book_id}")
async def upd_book_by_id(book_id: int, book_data: SBookUPD) -> dict:
    check = await BookDAO.update_book_by_id(book_id, title=book_data.title, description=book_data.description, publication_date=book_data.publication_date, available_copies=book_data.available_copies)
    if check:
        return {"message": f"Книга с ID {book_id} успешно обновлена!"}
    else:
        return {"message": "Ошибка при обновлении книги!"}


@router.delete("/dell/{book_id}")
async def dell_book_by_id(book_id: int) -> dict:
    check = await BookDAO.delete_book_by_id(book_id=book_id)
    if check:
        return {"message": f"Книга с iD {book_id} успешно удалена!"}
    else:
        return {"message": "Ошибка при удалении книги!"}
