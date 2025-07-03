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
        extension1 = Extension(id=1, name="epub")
        extension2 = Extension(id=2, name="fb2")
        extension3 = Extension(id=3, name="pdf")

        books = [
            Book(
                id=1,
                title="Преступление и наказание",
                year_written="1866",
                extensions=[extension1, extension2]
            ),
            Book(
                id=2,
                title="Талисман",
                year_written="2005",
                extensions=[extension1, extension3]
            ),
            Book(
                id=3,
                title="Война и мир",
                year_written="1869",
                extensions=[extension2]
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

