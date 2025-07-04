import pytest
import requests
from src.core.models import Book, Author, Genre
from src.core.models.base import Base
from src.core.session import session_maker, engine
from src.settings import BACKEND_URL


@pytest.fixture(scope="module", autouse=True)
def init_books_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with session_maker() as session:
        genre1 = Genre(id=1, name="Драма")
        genre2 = Genre(id=2, name="Детектив")
        genre3 = Genre(id=3, name="Роман")
        genre4 = Genre(id=4, name="Фантастика")

        author1 = Author(id=1, name="Федор Достоевский")
        author2 = Author(id=2, name="Лев Толстой")
        author3 = Author(id=3, name="Стивен Кинг")
        author4 = Author(id=4, name="Питер Страуб")

        books = [
            Book(
                id=1,
                title="Преступление и наказание",
                year_written="1866",
                authors=[author1],
                genres=[genre1, genre2],
            ),
            Book(
                id=2,
                title="Игрок",
                year_written="1866",
                authors=[author1],
                genres=[genre1],
            ),
            Book(
                id=3,
                title="Война и мир",
                year_written="1869",
                authors=[author2],
                genres=[genre3],
            ),
            Book(
                id=4,
                title="Талисман",
                year_written="2005",
                authors=[author3, author4],
                genres=[genre4],
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
    url = f"{BACKEND_URL}/books/{book_id}/genres"
    response = requests.get(url)

    assert response.status_code == 200
    genres = [genre["name"] for genre in response.json()]
    assert genres == expected_result
