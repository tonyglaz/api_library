from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class SBook(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=50,
                       description="Название книги, от 1 до 50 символов")
    description: str = Field(..., min_length=1, max_length=2000,
                             description="Описание книги, от 1 до 2000 символов")
    publication_date: int = Field(..., description="Год публикации книги")
    available_copies: int = Field(..., ge=0,
                                  description="Количество доступных книг")

    @field_validator("publication_date")
    def publication_date(cls, value):
        if value and value >= datetime.now().date().year:
            raise ValueError("Год публикации должен быть в прошлом")
        return value
    authors: List["Author"] = []
    genres:  List["Genre"] = []


class SBookADD(BaseModel):
    title: str = Field(..., min_length=1, max_length=50,
                       description="Название книги, от 1 до 50 символов")
    description: str = Field(..., min_length=1, max_length=2000,
                             description="Описание книги, от 1 до 2000 символов")
    publication_date: int = Field(..., description="Год публикации книги")
    available_copies: int = Field(..., ge=0,
                                  description="Количество доступных книг")

    @field_validator("publication_date")
    def validate_birthday(cls, value):
        if value and value >= datetime.now().date().year:
            raise ValueError("Год публикации должен быть в прошлом")
        return value


class SBookUPD(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=50,
                                 description="Название книги, от 1 до 50 символов")
    description: Optional[str] = Field(None, min_length=1, max_length=2000,
                                       description="Описание книги, от 1 до 2000 символов")
    publication_date: Optional[int] = Field(
        None, description="Год публикации книги")
    available_copies: Optional[int] = Field(None, ge=0,
                                            description="Количество доступных книг")

    @field_validator("publication_date")
    def validate_birthday(cls, value):
        if value and value >= datetime.now().date().year:
            raise ValueError("Год публикации должен быть в прошлом")
        return value
