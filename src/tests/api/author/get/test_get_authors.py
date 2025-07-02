import pytest
import requests
from src.core.models import Author, Book
from src.core.models.base import Base
from src.core.session import session_maker, engine
from src.settings import BACKEND_URL


@pytest.fixture(scope="module", autouse=True)
def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with session_maker() as session:
        authors = [
            Author(
                id=1,
                name="Федор Достоевский",
                books=[
                    Book(id=1, title="Преступление и наказание", year_written=1866),
                    Book(id=2, title="Игрок", year_written=1866),
                    Book(id=3, title="Идиот", year_written=1869)
                ]
            ),
            Author(
                id=2,
                name="Лев Толстой",
                books=[
                    Book(id=4, title="Война и мир", year_written=1869),
                    Book(id=5, title="Анна Каренина", year_written=1877)
                ]
            ),
            Author(
                id=3,
                name="Антон Чехов",
                books=[
                    Book(id=6, title="Вишневый сад", year_written=1904)
                ]
            ),
            Author(
                id=4,
                name="Иван Тургенев",
                books=[]
            )
        ]

        session.add_all(authors)
        session.commit()


@pytest.mark.parametrize(
    "params, expected_result",
    [
        ({}, ["Федор Достоевский", "Лев Толстой", "Антон Чехов", "Иван Тургенев"]),
        ({"limit": 2}, ["Федор Достоевский", "Лев Толстой"]),
        ({"offset": 1, "limit": 2}, ["Лев Толстой", "Антон Чехов"]),
        ({"starts_with": "Л"}, ["Лев Толстой"]),
        ({"starts_with": "И"}, ["Иван Тургенев"]),
        ({"starts_with": "Ан"}, ["Антон Чехов"]),
        ({"starts_with": "Алекс"}, []),
        ({"offset": 3}, ["Иван Тургенев"]),
    ]
)
def test_get_authors(params, expected_result: list[str]):
    url = f"{BACKEND_URL}/authors"
    response = requests.get(url, params=params)

    assert response.status_code == 200
    data = response.json()

    author_names = [author["name"] for author in data]
    assert author_names == expected_result
