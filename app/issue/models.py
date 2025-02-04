from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import date, datetime, timedelta, timezone
from typing import Optional
from app.users.models import User
from app.database import Base, int_pk


class BookIssue(Base):
    __tablename__ = "book_issues"

    id: Mapped[int_pk]
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    issue_date: Mapped[date] = mapped_column(
        default=datetime.now(),
        server_default=func.now(),
        nullable=False)
    due_date: Mapped[date] = mapped_column(
        default=lambda: datetime.now() + timedelta(days=14),
        server_default=func.now(),
        nullable=False)
    return_date: Mapped[Optional[date]]

    book: Mapped["Book"] = relationship("Book", back_populates="issued_user")
    user: Mapped["User"] = relationship(
        "User", back_populates="borrowed_books")

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'issue_date': self.issue_date,
            'due_date': self.due_date,
            'return_date': self.return_date,
            'book': self.book.title,
            'user': self.user.first_name
        }
