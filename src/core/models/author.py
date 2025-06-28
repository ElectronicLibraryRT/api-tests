from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship
)

from src.core.models.base import Base


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)

    books: Mapped[list['Book']] = relationship(
        secondary='books_authors',
        back_populates='authors'
    )