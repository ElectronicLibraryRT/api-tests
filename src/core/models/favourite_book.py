from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.core.models.base import Base


class FavouriteBook(Base):
    __tablename__ = 'favourite_books'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    added_ts: Mapped[datetime]

    book: Mapped['Book'] = relationship(
        back_populates='favourite_books',
        overlaps="favourites"
    )
    user: Mapped['User'] = relationship(
        back_populates='favourite_books',
        overlaps="readers"
    )