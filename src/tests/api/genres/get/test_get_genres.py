import pytest
import requests
from src.core.models import Genre
from src.core.models.base import Base
from src.core.session import session_maker, engine
from src.settings import BACKEND_URL


@pytest.fixture(scope="module", autouse=True)
def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with session_maker() as session:
        genres = [
            Genre(
                id=1,
                name="Роман",
            ),
            Genre(
                id=2,
                name="Комедия",
            ),
            Genre(
                id=3,
                name="Драма",
            ),
            Genre(
                id=4,
                name="Детектив",
            )
        ]

        session.add_all(genres)
        session.commit()


@pytest.mark.parametrize(
    "params, expected_result",
    [
        ({}, ["Роман", "Комедия", "Драма", "Детектив"]),
        ({"limit": 2}, ["Роман", "Комедия"]),
        ({"offset": 2}, ["Драма", "Детектив"]),
        ({"starts_with": "Д"}, ["Драма", "Детектив"]),
        ({"starts_with": "Коме"}, ["Комедия"]),
        ({"starts_with": "Трагедия"}, []),
        ({"offset": 1, "limit": 2}, ["Комедия", "Драма"])
    ]
)
def test_get_genres(params, expected_result: list[str]):
    url = f"{BACKEND_URL}/genres"
    response = requests.get(url, params=params)

    assert response.status_code == 200
    data = response.json()

    genre_names = [genre["name"] for genre in data]
    assert genre_names == expected_result
