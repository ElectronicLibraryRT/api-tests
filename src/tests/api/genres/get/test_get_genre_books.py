import pytest
import requests
from src.core.models import Genre, Book
from src.core.models.base import Base
from src.core.session import session_maker, engine
from src.settings import DATABASE_URL

BASE_URL = DATABASE_URL


@pytest.fixture(scope="module", autouse=True)
def init_genre_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with session_maker() as session:
        genres = [
            Genre(
                id=1,
                name="Классика",
                books=[
                    Book(id=1, title="Преступление и наказание", publication_date="1866"),
                    Book(id=2, title="Игрок", publication_date="1866"),
                    Book(id=3, title="Идиот", publication_date="1869")
                ]
            ),
            Genre(
                id=2,
                name="Роман",
                books=[
                    Book(id=4, title="Анна Каренина", publication_date="1877"),
                    Book(id=5, title="Война и мир", publication_date="1869")
                ]
            ),
            Genre(
                id=3,
                name="Драма",
                books=[
                    Book(id=6, title="Вишневый сад", publication_date="1904")
                ]
            ),
            Genre(
                id=4,
                name="Пустой жанр",
                books=[]
            )
        ]

        session.add_all(genres)
        session.commit()


@pytest.mark.parametrize(
    "genre_id, params, expected_result",
    [
        (1, {}, ["Преступление и наказание", "Игрок", "Идиот"]),
        (1, {"limit": 2}, ["Преступление и наказание", "Игрок"]),
        (1, {"offset": 1, "limit": 2}, ["Игрок", "Идиот"]),
        (1, {"starts_with": "И"}, ["Игрок", "Идиот"]),
        (1, {"starts_with": "Преступ"}, ["Преступление и наказание"]),

        (2, {}, ["Анна Каренина", "Война и мир"]),
        (2, {"limit": 1}, ["Анна Каренина"]),
        (2, {"offset": 1}, ["Война и мир"]),

        (3, {}, ["Вишневый сад"]),
        (3, {"starts_with": "Виш"}, ["Вишневый сад"]),
        (3, {"starts_with": "Сад"}, []),

        (4, {}, []),
    ]
)
def test_get_genre_books(genre_id: int, params, expected_result: list[str]):
    url = f"{BASE_URL}/genres/{genre_id}/books"
    response = requests.get(url, params=params)

    assert response.status_code == 200
    data = response.json()

    book_titles = [book["title"] for book in data]
    assert book_titles == expected_result
