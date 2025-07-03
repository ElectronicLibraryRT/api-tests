import pytest
import requests
from src.core.models import Book, Extension, Author, Genre
from src.core.models.base import Base
from src.core.session import session_maker, engine
from src.settings import BACKEND_URL


@pytest.fixture(scope="module", autouse=True)
def init_book_extensions_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with session_maker() as session:
        books = [
            Book(
                id=1,
                title="Преступление и наказание",
                year_written="1866",
                authors=[Author(id=1, name="Федор Достоевский")],
                genres=[
                    Genre(id=1, name="Драма"),
                    Genre(id=2, name="Детектив"),
                ],
                extensions=[
                    Extension(id=1, name="epub"),
                    Extension(id=2, name="fb2")
                ]
            ),
            Book(
                id=2,
                title="Талисман",
                year_written="2005",
                authors=[
                    Author(id=2, name="Стивен Кинг"),
                    Author(id=3, name="Питер Страуб"),
                ],
                genres=[Genre(id=4, name="Фантастика")],
                extensions=[
                    Extension(id=1, name="epub"),
                    Extension(id=3, name="pdf")
                ]
            ),
            Book(
                id=3,
                title="Война и мир",
                year_written="1869",
                authors=[Author(id=4, name="Лев Толстой")],
                genres=[Genre(id=3, name="Роман")],
                extensions=[Extension(id=2, name="fb2")]
            ),
        ]
        session.add_all(books)
        session.commit()


@pytest.mark.parametrize(
    "book_id, expected_result",
    [
        (1, ["epub", "fb2"]),
        (2, ["epub", "pdf"]),
        (3, ["fb2"])
    ]
)
def test_get_book_extensions(book_id: int, expected_result: list[str]):
    url = f"{BACKEND_URL}/books/{book_id}/extensions"
    response = requests.get(url)

    assert response.status_code == 200
    data = response.json()
    extensions = [item["extension"]["name"] for item in data]
    assert extensions == expected_result

