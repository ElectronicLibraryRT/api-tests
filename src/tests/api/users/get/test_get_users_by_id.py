import pytest
import requests
from src.core.models import User
from src.core.models.base import Base
from src.core.session import session_maker, engine
from src.settings import BACKEND_URL


@pytest.fixture(scope="module", autouse=True)
def init_users_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
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
            ),
            User(
                id=5,
                name="thomas",
                salt="salt5",
                password_hash="hash5",
                refresh_token_uuid="uuid5"
            )
        ]
        session.add_all(users)
        session.commit()


@pytest.mark.parametrize(
    "user_id, expected_status, expected_result",
    [
        (1,  200, "alice"),
        (2, 200, "bob"),
        (3, 200, "charlie"),
        (4, 200, "diana"),
        (5, 200, "thomas"),
        (999, 404, None),
    ]
)
def test_get_user_by_id(user_id: int, expected_status: int, expected_result: str | None):
    url = f"{BACKEND_URL}/users/{user_id}"
    response = requests.get(url)

    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert data["name"] == expected_result
