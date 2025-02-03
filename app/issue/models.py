from sqlalchemy import ForeignKey, func
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
        default=datetime.now(timezone.utc), server_default=func.now())
    due_date: Mapped[date] = mapped_column(default=lambda: datetime.now(
        timezone.utc) + timedelta(days=14), server_default=func.now())
    return_date: Mapped[Optional[date]]

    book: Mapped["Book"] = relationship("Book", back_populates="issues")
    user: Mapped["User"] = relationship(
        "User", back_populates="borrowed_books")
