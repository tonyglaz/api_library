from fastapi import APIRouter, Depends
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
    return result.to_dict()


@router.post("/add/")
async def add_book(book: SBookADD = Depends()) -> dict:
    check = await BookDAO.add_book(**book.model_dump())
    if check:
        return {"message": "Книга успешно добавлена!", "book": book}
    else:
        return {"message": "Ошибка при добавлении книги!"}


@router.put("/upd/{book_id}")
async def upd_book_by_id(book_id: int, book_data: SBookUPD = Depends()) -> dict:
    check = await BookDAO.update_book_by_id(book_id, book_data=book_data.model_dump(exclude_unset=True))
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
