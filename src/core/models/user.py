from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.core.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    salt: Mapped[str] = mapped_column(String(32))
    password_hash: Mapped[str] = mapped_column(String(512))
    refresh_token_uuid: Mapped[str] = mapped_column(String(32))


    read_history: Mapped[list['ReadHistory']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )

    read_books: Mapped[list['Book']] = relationship(
        secondary='read_history',
        back_populates='readers',
        viewonly = True,
        overlaps = "read_history"
    )

    favourite_books: Mapped[list['FavouriteBook']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )

    favourites: Mapped[list['Book']] = relationship(
        secondary='favourite_books',
        back_populates='favourited_by',
        viewonly=True,
        overlaps="favourite_books"
    )