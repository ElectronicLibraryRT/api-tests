from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.core.models.base import Base


class Extension(Base):
    __tablename__ = 'extensions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(8), unique=True)

    book_locations: Mapped[list['BookLocation']] = relationship(
        back_populates='extension',
        cascade='all, delete-orphan'
    )

    books: Mapped[list['Book']] = relationship(
        secondary='books_locations',
        back_populates='extensions',
        viewonly=True,
        overlaps="book_locations"
    )