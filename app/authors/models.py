# структура и схема данных связывающася с ORM (Object-Relational Mapping) sqlalchemy
from sqlalchemy.orm import Mapped
from datetime import date
from app.database import Base, int_pk


class Author(Base):
    __tablename__ = 'authors'
    # Аннотирования атрибутов класса, которые будут сопоставлены с колонками в базе данных
    id: Mapped[int_pk]
    name: Mapped[str]
    biography: Mapped[str]
    birthday: Mapped[date]

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'biography': self.biography,
            'birthday': self.birthday
        }
