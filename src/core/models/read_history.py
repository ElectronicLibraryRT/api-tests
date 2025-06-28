from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.core.models.base import Base


class ReadHistory(Base):
    __tablename__ = 'read_history'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    last_read_ts: Mapped[datetime]

    book: Mapped['Book'] = relationship(
        back_populates='read_history',
        overlaps="read_books"
    )

    user: Mapped['User'] = relationship(
        back_populates='read_history',
        overlaps="favourited_by"
    )