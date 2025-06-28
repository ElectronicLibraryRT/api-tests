from datetime import date

from sqlalchemy import (
    String,
    Date,
    UniqueConstraint
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship
)

from src.core.models import FavouriteBook
from src.core.models.base import Base


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(128))
    publication_date: Mapped[date | None]

    authors: Mapped[list['Author']] = relationship(
        secondary='books_authors',
        back_populates='books'
    )
    genres: Mapped[list['Genre']] = relationship(
        secondary='books_genres',
        back_populates='books'
    )



    book_locations: Mapped[list['BookLocation']] = relationship(
        back_populates='book',
        cascade='all, delete-orphan'
    )
    extensions: Mapped[list['Extension']] = relationship(
        secondary='books_locations',
        back_populates='books',
        viewonly=True,
        overlaps="book_locations"
    )

    read_history: Mapped[list['ReadHistory']] = relationship(
        back_populates='book',
        cascade='all, delete-orphan'
    )
    readers: Mapped[list['User']] = relationship(
        secondary='read_history',
        back_populates='read_books',
        viewonly = True,
        overlaps = "read_history"
    )



    favourite_books: Mapped[list['FavouriteBook']] = relationship(
        back_populates='book',
        cascade='all, delete-orphan'
    )
    favourited_by: Mapped[list['User']] = relationship(
        secondary='favourite_books',
        back_populates='favourites',
        viewonly = True,
        overlaps = "favourite_books"
    )


    __table_args__ = (
        UniqueConstraint('title', 'publication_date', name='books_ak_1'),
    )