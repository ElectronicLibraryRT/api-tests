import pytest
import requests
from src.core.models import Book, Author
from src.core.session import session_maker

BASE_URL = "http://elibrary.ddns.net"


@pytest.fixture(scope="module", autouse=True)
def init_books_db():
    with session_maker() as session:
        books = [
            Book(
                id=1,
                title="Преступление и наказание",
                publication_date="1866",
                authors=[Author(id=1, name="Федор Достоевский")]
            ),
            Book(
                id=2,
                title="Игрок",
                publication_date="1866",
                authors=[Author(id=1, name="Федор Достоевский")]
            ),
            Book(
                id=3,
                title="Война и мир",
                publication_date="1869",
                authors=[Author(id=1, name="Лев Толстой")]
            ),
            Book(
                id=4,
                title="Талисман",
                publication_date="2005",
                authors=[
                    Author(id=2, name="Стивен Кинг"),
                    Author(id=3, name="Питер Страуб"),
                ]
            ),
        ]
        session.add_all(books)
        session.commit()


@pytest.mark.parametrize(
    "book_id, expected_result",
    [
        (1, ["Федор Достоевский"]),
        (4, ["Стивен Кинг", "Питер Страуб"]),
        (2, ["Лев Толстой"]),
    ]
)
def test_get_book_authors(book_id: int, expected_result: list[str]):
    url = f"{BASE_URL}/books/{book_id}/authors"
    response = requests.get(url)

    assert response.status_code == 200
    authors = [author["name"] for author in response.json()]
    assert authors == expected_result
