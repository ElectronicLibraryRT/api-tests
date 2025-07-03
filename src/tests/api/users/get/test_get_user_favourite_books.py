import pytest
import requests
from src.core.models import User, Book, Genre, Extension, FavouriteBook
from src.core.session import session_maker
from src.settings import BACKEND_URL


@pytest.fixture(scope="module", autouse=True)
def init_users_db():
    with session_maker() as session:
        users = [
            User(
                id=1,
                name="alice",
                salt="salt1",
                password_hash="hash1",
                refresh_token_uuid="uuid1",
                favourites=[
                    Book(
                        id=1,
                        title="Преступление и наказание",
                        genre=[Genre(id=1, name="Детектив")],
                        year_written="1866",
                        extension=[Extension(id=1, name="fb2")]
                    ),
                    Book(
                        id=2,
                        title="Игрок",
                        genre=[Genre(id=1, name="Драма")],
                        year_written="1866",
                        extension=[Extension(id=1, name="fb2")]
                    )
                ],
                favourite_books=[
                    FavouriteBook(
                        user_id=1,
                        book_id=1,
                        added_ts="2025-07-02 10:23:54"
                    ),
                    FavouriteBook(
                        user_id=1,
                        book_id=2,
                        added_ts="2025-03-02 10:23:54"
                    ),
                ]
            ),
            User(
                id=2,
                name="bob",
                salt="salt2",
                password_hash="hash2",
                refresh_token_uuid="uuid2",
                favourites=[
                    Book(
                        id=2,
                        title="Игрок",
                        genre=[Genre(id=1, name="Драма")],
                        year_written="1866",
                        extension=[Extension(id=1, name="fb2")]
                    )
                ],
                favourite_books=[FavouriteBook(user_id=2, book_id=2, added_ts="2025-06-02 10:23:54")]
            ),
            User(
                id=3,
                name="charlie",
                salt="salt3",
                password_hash="hash3",
                refresh_token_uuid="uuid3",
                favourites=[
                    Book(
                        id=1,
                        title="Преступление и наказание",
                        genre=[Genre(id=1, name="Детектив")],
                        year_written="1866",
                        extension=[Extension(id=1, name="fb2")]
                    )
                ],
                favourite_books=[FavouriteBook(user_id=3, book_id=1, added_ts="2025-05-02 10:23:54")]
            ),
            User(
                id=4,
                name="diana",
                salt="salt4",
                password_hash="hash4",
                refresh_token_uuid="uuid4",
                favourites=[
                    Book(
                        id=3,
                        title="Анна Каренина",
                        genre=[Genre(id=3, name="Hjvfy")],
                        year_written="1877",
                        extension=[Extension(id=1, name="fb2")]
                    )
                ],
                favourite_books=[FavouriteBook(user_id=4, book_id=3, added_ts="2025-01-02 10:23:54")]
            )
        ]
        session.add_all(users)
        session.commit()


@pytest.mark.parametrize(
    "user_id, expected_books, expected_ts",
    [
        (1, ["Преступление и наказание", "Игрок"], ["2025-07-02 10:23:54", "2025-03-02 10:23:54"]),
        (2, ["Игрок"], ["2025-06-02 10:23:54"]),
        (3, ["Преступление и наказание"], ["2025-05-02 10:23:54"]),
        (4, ["Анна Каренина"], "2025-01-02 10:23:54"),
    ]
)
def test_get_user_read_history(user_id, expected_books: list[str], expected_ts: list[str]):
    url = f"{BACKEND_URL}/users/{user_id}/favourite_books"
    response = requests.get(url)

    assert response.status_code == 200
    data = response.json()

    titles = [item["favourites"]["title"] for item in data]
    assert titles == expected_books

    time_stamps = [item["favourite_books"]["added_ts"] for item in data]
    assert time_stamps == expected_ts
