from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.core.models.base import Base


class BookGenre(Base):
    __tablename__ = 'books_genres'

    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey('genres.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )