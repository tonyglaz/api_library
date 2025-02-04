from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk


class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str_uniq]
    password: Mapped[str]

    is_user: Mapped[bool] = mapped_column(
        default=True, server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(
        default=False, server_default=text('false'), nullable=False)

    borrowed_books: Mapped[list["BookIssue"]] = relationship(
        "BookIssue", back_populates="user")

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'is_user': self.is_user,
            'is_admin': self.is_admin,
            'borrowed_books': [issue.book.title for issue in self.borrowed_books] if self.borrowed_books else None
        }
