import pytest
import requests
from src.core.models import User
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
                refresh_token_uuid="uuid1"
            ),
            User(
                id=2,
                name="bob",
                salt="salt2",
                password_hash="hash2",
                refresh_token_uuid="uuid2"
            ),
            User(
                id=3,
                name="charlie",
                salt="salt3",
                password_hash="hash3",
                refresh_token_uuid="uuid3"
            ),
            User(
                id=4,
                name="diana",
                salt="salt4",
                password_hash="hash4",
                refresh_token_uuid="uuid4"
            )
        ]
        session.add_all(users)
        session.commit()


@pytest.mark.parametrize(
    "params, expected_result",
    [
        ({}, ["alice", "bob", "charlie", "diana"]),
        ({"limit": 2}, ["alice", "bob"]),
        ({"offset": 2}, ["charlie", "diana"]),
        ({"starts_with": "a"}, ["alice"]),
        ({"starts_with": "z"}, []),
    ]
)
def test_get_users(params, expected_result: list[str]):
    url = f"{BACKEND_URL}/users"
    response = requests.get(url, params=params)

    assert response.status_code == 200
    data = response.json()

    usernames = [user["name"] for user in data]
    assert usernames == expected_result
