# организация маршрутов (эндпоинтов) приложения
from fastapi import APIRouter, Depends
from app.authors.dao import AuthorDAO
from app.authors.schemas import SAuthor, SAuthorADD, SAuthorUPD


router = APIRouter(prefix="/authors", tags=["Работа с авторами"])


@router.get("/", summary="Получить всех авторов")
async def get_all_authors():
    return await AuthorDAO.find_all_authors()


@router.get("/{id}/", summary="Получить одного автора по id")
async def get_author_by_id(author_id: int):
    result = await AuthorDAO.find_one_or_none_by_id(author_id)
    if result is None:
        return {"message": f"Автор с ID {author_id} не найден!"}
    return result


@router.post("/add/")
async def add_author(author: SAuthorADD = Depends()) -> dict:
    check = await AuthorDAO.add_author(**author.model_dump())
    if check:
        return {"message": "Автор успешно добавлен!", "author": author}
    else:
        return {"message": "Ошибка при добавлении автора!"}


@router.put("/upd/{author_id}")
async def upd_author_by_id(author_id: int, author_data: SAuthorUPD = Depends()) -> dict:
    # name = author_data.name,birthday = author_data.birthday,biography=author_data.biography
    check = await AuthorDAO.update_author_by_id(author_id,  author_data=author_data.model_dump(exclude_unset=True))
    if check:
        return {"message": f"Автор с ID {author_id} успешно обновлен!"}
    else:
        return {"message": "Ошибка при обновлении автора!"}


@router.delete("/dell/{author_id}")
async def dell_author_by_id(author_id: int) -> dict:
    check = await AuthorDAO.delete_author_by_id(author_id=author_id)
    if check:
        return {"message": f"Автор с iD {author_id} успешно удален!"}
    else:
        return {"message": "Ошибка при удалении автора!"}
