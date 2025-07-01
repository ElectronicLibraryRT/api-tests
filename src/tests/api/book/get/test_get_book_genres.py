import pytest
import requests
from src.core.models import Book, Author, Genre
from src.core.session import session_maker
from src.settings import DATABASE_URL

BASE_URL = DATABASE_URL


@pytest.fixture(scope="module", autouse=True)
def init_books_db():
    with session_maker() as session:
        books = [
            Book(
                id=1,
                title="Преступление и наказание",
                publication_date="1866",
                authors=[Author(id=1, name="Федор Достоевский")],
                genres=[
                    Genre(id=1, name="Драма"),
                    Genre(id=2, name="Детектив"),
                ]
            ),
            Book(
                id=2,
                title="Игрок",
                publication_date="1866",
                authors=[Author(id=1, name="Федор Достоевский")],
                genres=[Genre(id=1, name="Драма")]
            ),
            Book(
                id=3,
                title="Война и мир",
                publication_date="1869",
                authors=[Author(id=1, name="Лев Толстой")],
                genres=[Genre(id=3, name="Роман")]
            ),
            Book(
                id=4,
                title="Талисман",
                publication_date="2005",
                authors=[
                    Author(id=2, name="Стивен Кинг"),
                    Author(id=3, name="Питер Страуб"),
                ],
                genres=[Genre(id=4, name="Фантастика")]
            ),
        ]
        session.add_all(books)
        session.commit()


@pytest.mark.parametrize(
    "book_id, expected_result",
    [
        (1, ["Драма", "Детектив"]),
        (2, ["Драма"]),
        (3, ["Роман"]),
        (4, ["Фантастика"]),
    ]
)
def test_get_book_genres(book_id: int, expected_result: list[str]):
    url = f"{BASE_URL}/books/{book_id}/genres"
    response = requests.get(url)

    assert response.status_code == 200
    genres = [genre["name"] for genre in response.json()]
    assert genres == expected_result
