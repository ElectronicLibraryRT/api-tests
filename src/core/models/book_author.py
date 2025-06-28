from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from src.core.models.base import Base

class BookAuthor(Base):
    __tablename__ = 'books_authors'

    author_id: Mapped[int] = mapped_column(
        ForeignKey('authors.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )