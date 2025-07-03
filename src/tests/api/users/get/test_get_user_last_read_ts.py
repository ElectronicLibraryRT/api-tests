import pytest
import requests
from src.core.models import User, Book, Genre, Extension, ReadHistory
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
                read_books=[
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
                read_history=[
                    ReadHistory(
                        user_id=1,
                        book_id=1,
                        last_read_ts="2025-07-02 10:23:54"
                    ),
                    ReadHistory(
                        user_id=1,
                        book_id=2,
                        last_read_ts="2025-03-02 10:23:54"
                    ),
                ]
            ),
            User(
                id=2,
                name="bob",
                salt="salt2",
                password_hash="hash2",
                refresh_token_uuid="uuid2",
                read_books=[
                    Book(
                        id=2,
                        title="Игрок",
                        genre=[Genre(id=1, name="Драма")],
                        year_written="1866",
                        extension=[Extension(id=1, name="fb2")]
                    )
                ],
                read_history=[ReadHistory(user_id=2, book_id=2, last_read_ts="2025-06-02 10:23:54")]
            ),
            User(
                id=3,
                name="charlie",
                salt="salt3",
                password_hash="hash3",
                refresh_token_uuid="uuid3",
                read_books=[
                    Book(
                        id=1,
                        title="Преступление и наказание",
                        genre=[Genre(id=1, name="Детектив")],
                        year_written="1866",
                        extension=[Extension(id=1, name="fb2")]
                    )
                ],
                read_history=[ReadHistory(user_id=3, book_id=1, last_read_ts="2025-05-02 10:23:54")]
            ),
            User(
                id=4,
                name="diana",
                salt="salt4",
                password_hash="hash4",
                refresh_token_uuid="uuid4",
                read_books=[
                    Book(
                        id=3,
                        title="Анна Каренина",
                        genre=[Genre(id=3, name="Hjvfy")],
                        year_written="1877",
                        extension=[Extension(id=1, name="fb2")]
                    )
                ],
                read_history=[ReadHistory(user_id=4, book_id=3, last_read_ts="2025-01-02 10:23:54")]
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
    url = f"{BACKEND_URL}/users/{user_id}/read_history/{book_id}"
    response = requests.get(url)

    assert response.status_code == expected_status

    if expected_status == 200:
        data = response.json()
        assert data["last_read_ts"] == expected_ts
