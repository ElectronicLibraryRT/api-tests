import pytest
import requests
from src.core.models import Book
from src.core.session import session_maker
from src.settings import DATABASE_URL

BASE_URL = DATABASE_URL


@pytest.fixture(scope="module", autouse=True)
def init_books_db():
    with session_maker() as session:
        books = [
            Book(id=1, title="Преступление и наказание", publication_date="1866"),
            Book(id=2, title="Игрок", publication_date="1866"),
            Book(id=3, title="Идиот", publication_date="1869"),
            Book(id=4, title="Анна Каренина", publication_date="1877"),
            Book(id=5, title="Война и мир", publication_date="1869"),
            Book(id=6, title="Вишневый сад", publication_date="1904")
        ]
        session.add_all(books)
        session.commit()


@pytest.mark.parametrize(
    "params, expected_titles",
    [
        ({}, ["Преступление и наказание", "Игрок", "Идиот", "Анна Каренина", "Война и мир", "Вишневый сад"]),
        ({"limit": 3}, ["Преступление и наказание", "Игрок", "Идиот"]),
        ({"offset": 3}, ["Анна Каренина", "Война и мир", "Вишневый сад"]),
        ({"offset": 2, "limit": 2}, ["Идиот", "Анна Каренина"]),
        ({"starts_with": "И"}, ["Игрок", "Идиот"]),
        ({"starts_with": "В"}, ["Война и мир", "Вишневый сад"]),
        ({"starts_with": "Ц"}, []),
    ]
)
def test_get_books(params, expected_titles):
    url = f"{BASE_URL}/books"
    response = requests.get(url, params=params)

    assert response.status_code == 200
    data = response.json()

    titles = [book["title"] for book in data]
    assert titles == expected_titles
