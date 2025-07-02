import pytest
import requests
from src.core.models import Book, Author, Extension, Genre
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
                year_written="1866",
                authors=[Author(id=1, name="Федор Достоевский")],
                genres=[Genre(id=1, name="No matter")],
                extensions=[Extension(id=1, name="fb2")],
            ),
            Book(
                id=2,
                title="Игрок",
                year_written="1866",
                authors=[Author(id=1, name="Федор Достоевский")],
                genres=[Genre(id=1, name="No matter")],
                extensions=[Extension(id=1, name="fb2")],
            ),
            Book(
                id=3,
                title="Война и мир",
                year_written="1869",
                authors=[Author(id=2, name="Лев Толстой")],
                genres=[Genre(id=1, name="No matter")],
                extensions=[Extension(id=1, name="fb2")],
            ),
            Book(
                id=4,
                title="Талисман",
                year_written="2005",
                authors=[
                    Author(id=3, name="Стивен Кинг"),
                    Author(id=4, name="Питер Страуб"),
                ],
                genres=[Genre(id=1, name="No matter")],
                extensions=[Extension(id=1, name="fb2")],
            ),
        ]
        session.add_all(books)
        session.commit()


@pytest.mark.parametrize(
    "book_id, expected_result",
    [
        (1, ["Федор Достоевский"]),
        (4, ["Стивен Кинг", "Питер Страуб"]),
        (3, ["Лев Толстой"]),
    ]
)
def test_get_book_authors(book_id: int, expected_result: list[str]):
    url = f"{BACKEND_URL}/books/{book_id}/authors"
    response = requests.get(url)

    assert response.status_code == 200
    authors = [author["name"] for author in response.json()]
    assert authors == expected_result
