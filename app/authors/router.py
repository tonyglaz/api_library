# организация маршрутов (эндпоинтов) приложения
from fastapi import APIRouter
from app.authors.dao import AuthorDAO
from app.authors.schemas import Author


router = APIRouter(prefix='/authors', tags=['Работа с авторами'])


@router.get('/', summary="Получить всех авторов")
async def get_all_authors() -> list[Author]:
    return await AuthorDAO.find_all()


@router.get("/{id}", summary="Получить одного автора по id")
async def get_author_by_id(author_id: int) -> Author | dict:
    result = await AuthorDAO.find_one_or_none_by_id(author_id)
    if result is None:
        return {'message': f'Автор с ID {author_id} не найден!'}
    return result
