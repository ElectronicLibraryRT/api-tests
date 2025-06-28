from sqlalchemy import (
    String,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.core.models.base import Base


class BookLocation(Base):
    __tablename__ = 'books_locations'

    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    extension_id: Mapped[int] = mapped_column(
        ForeignKey('extensions.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    location: Mapped[str] = mapped_column(String(256), unique=True)


    book: Mapped['Book'] = relationship(
        back_populates='book_locations',
        overlaps="extensions"
    )
    extension: Mapped['Extension'] = relationship(
        back_populates='book_locations',
        overlaps="books"
    )