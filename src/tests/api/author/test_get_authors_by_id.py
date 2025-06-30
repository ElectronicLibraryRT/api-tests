import pytest
import requests
from src.core.models import Author, Book
from src.core.session import session_maker

BASE_URL = "http://elibrary.ddns.net"


@pytest.fixture(scope="module", autouse=True)
def init_db():
    with session_maker() as session:
        authors = [
            Author(
                id=1,
                name="Федор Достоевский",
                books=[
                    Book(
                        id=1,
                        title="Преступление и наказание",
                        publication_date="1866"
                    ),
                    Book(
                        id=2,
                        title="Игрок",
                        publication_date="1866"
                    )
                ]
            ),
            Author(name="Габриэль Гарсиа Маркес"),
            Author(name="Харуки Мураками"),
            Author(name="Джейн Остин"),
        ]

        session.add(authors)
        session.commit()


@pytest.mark.parametrize(
    "author_id, expected_status, expected_result",
    [
        (1, 200, "Федор Достоевский"),
        (2, 200, "Габриэль Гарсиа Маркес"),
        (3, 200, "Харуки Мураками"),
        (4, 200, "Джейн Остин"),
        (999, 404, None),

    ]
)
def test_get_authors_by_id(author_id: int, expected_status: int, expected_result: str | None):
    url = f"{BASE_URL}/authors/{author_id}"
    response = requests.get(url)

    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert data["name"] == expected_result
