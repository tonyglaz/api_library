# структура и схема данных связывающася с ORM (Object-Relational Mapping) sqlalchemy
from sqlalchemy.orm import Mapped, relationship
from datetime import date
from app.database import Base, int_pk
from app.books.models import Book


class Author(Base):
    __tablename__ = "authors"
    # Аннотирования атрибутов класса, которые будут сопоставлены с колонками в базе данных
    id: Mapped[int_pk]
    name: Mapped[str]
    biography: Mapped[str]
    birthday: Mapped[date]

    books: Mapped[list["Book"]] = relationship("Book", secondary="book_authors",
                                               back_populates="authors")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'biography': self.biography,
            'birthday': self.birthday,
            'books': [book.title for book in self.books] if self.books else None
        }
