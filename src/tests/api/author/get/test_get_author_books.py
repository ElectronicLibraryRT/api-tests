import pytest
import requests
from src.core.models import Author, Book
from src.core.models.base import Base
from src.core.session import session_maker, engine
from src.settings import DATABASE_URL

BASE_URL = DATABASE_URL


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
                    Book(id=1, title="Преступление и наказание", publication_date="1866-01-01"),
                    Book(id=2, title="Игрок", publication_date="1866-01-01"),
                    Book(id=3, title="Идиот", publication_date="1869-01-01")
                ]
            ),
            Author(
                id=2,
                name="Лев Толстой",
                books=[
                    Book(id=4, title="Война и мир", publication_date="1869-01-01"),
                    Book(id=5, title="Анна Каренина", publication_date="1877-01-01")
                ]
            ),
            Author(
                id=3,
                name="Антон Чехов",
                books=[
                    Book(id=6, title="Вишневый сад", publication_date="1904-01-01")
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
    "author_id, params, expected_result",
    [
        (1, {}, ["Преступление и наказание", "Игрок", "Идиот"]),
        (1, {"limit": 2}, ["Преступление и наказание", "Игрок"]),
        (1, {"offset": 1, "limit": 2}, ["Игрок", "Идиот"]),
        (1, {"starts_with": "И"}, ["Игрок", "Идиот"]),
        (1, {"starts_with": "Преступ"}, ["Преступление и наказание"]),

        (2, {}, ["Война и мир", "Анна Каренина"]),
        (2, {"limit": 1}, ["Война и мир"]),
        (2, {"offset": 1}, ["Анна Каренина"]),

        (3, {}, ["Вишневый сад"]),
        (3, {"starts_with": "Виш"}, ["Вишневый сад"]),
        (3, {"starts_with": "Сад"}, []),

        (4, {}, []),
    ]
)
def test_get_author_books(author_id: int, params, expected_result: list[str]):
    url = f"{BASE_URL}/authors/{author_id}/books"
    response = requests.get(url, params=params)

    assert response.status_code == 200
    data = response.json()

    book_titles = [book["title"] for book in data]
    assert book_titles == expected_result
