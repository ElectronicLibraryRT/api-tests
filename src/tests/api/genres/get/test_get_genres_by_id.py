import pytest
import requests
from src.core.models import Author, Book, Genre
from src.core.session import session_maker

BASE_URL = "http://elibrary.ddns.net"


@pytest.fixture(scope="module", autouse=True)
def init_db():
    with session_maker() as session:
        genres = [
            Genre(
                id=1,
                name="Роман"
            ),
            Genre(
                id=2,
                name="Комедия"
            ),
            Genre(
                id=3,
                name="Драма"
            )
        ]

        session.add_all(genres)
        session.commit()


@pytest.mark.parametrize(
    "genre_id, expected_status, expected_result",
    [
        (1, 200, "Роман"),
        (3, 200, "Драма"),
        (999, 404, None),
    ]
)
def test_get_genre_by_id(genre_id: int, expected_status: int, expected_result: str | None):
    url = f"{BASE_URL}/genres/{genre_id}"
    response = requests.get(url)

    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert data["name"] == expected_result
