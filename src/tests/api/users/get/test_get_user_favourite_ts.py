import pytest
import requests
from src.core.models import User, Book, Genre, Extension, FavouriteBook
from src.core.models.base import Base
from src.core.session import session_maker, engine
from src.settings import BACKEND_URL


@pytest.fixture(scope="module", autouse=True)
def init_users_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with session_maker() as session:
        genre1 = Genre(id=1, name="Детектив")
        genre2 = Genre(id=2, name="Драма")
        extension_fb2 = Extension(id=1, name="fb2")

        book1 = Book(
            id=1,
            title="Преступление и наказание",
            year_written=1866,
            genres=[genre1],
            extensions=[extension_fb2]
        )
        book2 = Book(
            id=2,
            title="Игрок",
            year_written=1866,
            genres=[genre2],
            extensions=[extension_fb2]
        )
        book3 = Book(
            id=3,
            title="Анна Каренина",
            year_written=1877,
            genres=[genre2],
            extensions=[extension_fb2]
        )

        users = [
            User(
                id=1,
                name="alice",
                salt="salt1",
                password_hash="hash1",
                refresh_token_uuid="uuid1",
                favourite_books=[
                    FavouriteBook(book=book1, added_ts="2025-07-02 10:23:54"),
                    FavouriteBook(book=book2, added_ts="2025-03-02 10:23:54"),
                ]
            ),
            User(
                id=2,
                name="bob",
                salt="salt2",
                password_hash="hash2",
                refresh_token_uuid="uuid2",
                favourite_books=[
                    FavouriteBook(book=book2, added_ts="2025-06-02 10:23:54")
                ]
            ),
            User(
                id=3,
                name="charlie",
                salt="salt3",
                password_hash="hash3",
                refresh_token_uuid="uuid3",
                favourite_books=[
                    FavouriteBook(book=book1, added_ts="2025-05-02 10:23:54")
                ]
            ),
            User(
                id=4,
                name="diana",
                salt="salt4",
                password_hash="hash4",
                refresh_token_uuid="uuid4",
                favourite_books=[
                    FavouriteBook(book=book3, added_ts="2025-01-02 10:23:54")
                ]
            )
        ]

        session.add_all(users)
        session.commit()


@pytest.mark.parametrize(
    "user_id, book_id, expected_status, expected_ts",
    [
        (1, 1, 200, "2025-07-02 10:23:54"),
        (1, 2, 200, "2025-03-02 10:23:54"),
        (2, 2, 200, "2025-06-02 10:23:54"),
        (3, 1, 200, "2025-05-02 10:23:54"),
        (1, 4, 404, None),
        (4, 1, 404, None),
        (999, 1, 404, None),
        (1, 999, 404, None),
    ]
)
def test_get_read_timestamp(user_id: int, book_id: int, expected_status: int, expected_ts: str | None):
    url = f"{BACKEND_URL}/users/{user_id}/favourite_books/{book_id}"
    response = requests.get(url)

    assert response.status_code == expected_status

    if expected_status == 200:
        data = response.json()
        assert data["added_ts"] == expected_ts
