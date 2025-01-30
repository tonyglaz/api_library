# модели Pydantic для валидации входящих и исходящих данных API
from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator
from app.books.schemas import SBook
from typing import List, Optional


class SAuthor(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50,
                      description="Имя автора,от 1 до 50 символов")
    biography: str = Field(..., min_length=1, max_length=2000,
                           description="Имя автора,от 1 до 2000 символов")
    birthday: date = Field(..., description="Дата рождения автора")

    books: List["SBook"] = []

    @field_validator("birthday")
    def validate_birthday(cls, value):
        if value and value >= datetime.now().date():
            raise ValueError("Дата рождения должна быть в прошлом")
        return value


class SAuthorADD(BaseModel):
    name: str = Field(..., min_length=1, max_length=50,
                      description="Имя автора,от 1 до 50 символов")
    biography: str = Field(..., min_length=1, max_length=2000,
                           description="Имя автора,от 1 до 2000 символов")
    birthday: date = Field(...,
                           description="Дата рождения автора в формате ГГГГ-ММ-ДД")

    @field_validator("birthday")
    def validate_birthday(cls, value):
        if value and value >= datetime.now().date():
            raise ValueError("Дата рождения должна быть в прошлом")
        return value


class SAuthorUPD(BaseModel):
    name: Optional[str] = Field(
        None, description="Имя автора,от 1 до 50 символов")
    biography: Optional[str] = Field(
        None, description="Имя автора,от 1 до 2000 символов")
    birthday: Optional[date] = Field(None, description="Дата рождения автора")

    @field_validator("birthday")
    def validate_birthday(cls, value):
        if value and value >= datetime.now().date():
            raise ValueError("Дата рождения должна быть в прошлом")
        return value
