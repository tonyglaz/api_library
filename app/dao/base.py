# универсальные методы
from sqlalchemy import update,delete
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload,selectinload
from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            authors = await session.execute(query)
            return authors.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, author_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=author_id).options(selectinload(cls.model.books))
            result = await session.execute(query)
            book = result.scalars().one_or_none()
            book_data = []
            book_data.append(book.to_dict())                   
            return book_data

    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            # автоматически начинает транзакцию и завершает её после выхода из блока, что гарантирует целостность данных.
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)  # Добавляем новый экземпляр в сессию
                try:  # Пытаемся зафиксировать изменения в базе данных
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()  # В случае ошибки откатываем транзакцию
                    raise e
                return new_instance

    @classmethod
    async def update(cls, filter_by, **values):#условия фильтрации и значения для обновления
        async with async_session_maker() as session:
            async with session.begin():
                # query = (update(cls.model)...): Создаётся запрос на обновление записей в таблице, связанной с моделью cls.model.
                # .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()]): Добавляются условия фильтрации,
                # чтобы обновить только те записи, которые соответствуют заданным условиям
                #.values(**values): Устанавливаются новые значения для обновляемых записей.
                #.execution_options(synchronize_session="fetch"): Опция, чтобы синхронизировать состояние сессии с базой данных после выполнения запроса.
                query = (
                    update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
                )
            result = await session.execute(query)#Выполняется запрос на обновление
            try:
                await session.commit()# Сохраняются изменения в базе данных.
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount

    @classmethod
    async def delete(cls,delete_all: bool = False,**filter_by):
        if not delete_all and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления.")
        
        async with async_session_maker() as session:
            async with session.begin():
                query = delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount
