import pytest
import requests
from src.core.models import Book
from src.core.models.base import Base
from src.core.session import session_maker, engine
from src.settings import BACKEND_URL


@pytest.fixture(scope="module", autouse=True)
def init_books_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with session_maker() as session:
        books = [
            Book(
                id=1,
                title="Преступление и наказание",
                year_written=1866,
            ),
            Book(
                id=2,
                title="Игрок",
                year_written=1866,
            ),
            Book(
                id=3,
                title="Идиот",
                year_written=1869,
            ),
            Book(
                id=4,
                title="Анна Каренина",
                year_written=1877,
            ),
            Book(
                id=5,
                title="Война и мир",
                year_written=1869,
            ),
            Book(
                id=6,
                title="Вишневый сад",
                year_written=1904,
            )
        ]
        session.add_all(books)
        session.commit()


@pytest.mark.parametrize(
    "book_id, expected_status, expected_title",
    [
        (1, 200, "Преступление и наказание"),
        (5, 200, "Война и мир"),
        (999, 404, None),
    ]
)
def test_get_book_by_id(book_id: int, expected_status: int, expected_title: str | None):
    url = f"{BACKEND_URL}/books/{book_id}"
    response = requests.get(url)

    assert response.status_code == expected_status

    if expected_status == 200:
        book = response.json()
        assert book["title"] == expected_title
