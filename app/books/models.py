from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.database import Base, int_pk, str_null_true
from app.issue.models import BookIssue


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int_pk]
    name: Mapped[str]

    books: Mapped[list["BookGenre"]] = relationship(
        "BookGenre", back_populates="genre")

    def str(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"

    def repr(self):
        return str(self)


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int_pk]
    title: Mapped[str]
    description: Mapped[str]
    publication_date: Mapped[int]
    available_copies: Mapped[int]
    authors: Mapped[list["Author"]] = relationship(
        "Author", secondary="book_authors", back_populates="books")
    genres: Mapped[list["BookGenre"]] = relationship(
        "BookGenre", back_populates="book")
    issues: Mapped[list["BookIssue"]] = relationship(
        "BookIssue", back_populates="book")

    def str(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title})"

    def repr(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'publication_date': self.publication_date,
            'available_copies': self.available_copies,
            'authors': [author.name for author in self.authors] if self.authors else None,
            'genres:': [book_genre.genre.name for book_genre in self.genres if book_genre.genre] if self.genres else None
        }


class BookGenre(Base):
    __tablename__ = "book_genres"

    book_id: Mapped[int_pk] = mapped_column(ForeignKey('books.id'))
    genre_id: Mapped[int_pk] = mapped_column(ForeignKey('genres.id'))

    book: Mapped["Book"] = relationship("Book", back_populates="genres")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")


class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id: Mapped[int_pk] = mapped_column(ForeignKey('books.id'))
    author_id: Mapped[int_pk] = mapped_column(ForeignKey('authors.id'))
