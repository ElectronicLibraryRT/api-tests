import os
import boto3
import pytest
import requests
from src.core.models import Book, Extension, BookLocation
from src.core.models.base import Base
from botocore.client import Config
from src.core.session import session_maker, engine
from src.settings import BACKEND_URL, MINIO_HOST, MINIO_PORT, MINIO_ROOT_USER, MINIO_ROOT_PASSWORD, MINIO_BUCKET

FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')


@pytest.fixture(scope="module", autouse=True)
def minio_client():
    client = boto3.client(
        's3',
        endpoint_url=f'http://{MINIO_HOST}:{MINIO_PORT}',
        aws_access_key_id=MINIO_ROOT_USER,
        aws_secret_access_key=MINIO_ROOT_PASSWORD,
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )

    for file_name in os.listdir(FILES_DIR):
        local_path = os.path.join(FILES_DIR, file_name)
        if not os.path.isfile(local_path):
            continue
        key = file_name
        try:
            client.head_object(Bucket=MINIO_BUCKET, Key=key)
        except client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                with open(local_path, 'rb') as data:
                    client.put_object(Bucket=MINIO_BUCKET, Key=key, Body=data)
            else:
                raise

    return client


@pytest.fixture(scope="module", autouse=True)
def init_book_extensions_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with session_maker() as session:
        extension1 = Extension(id=1, name="epub")
        extension2 = Extension(id=2, name="fb2")
        extension3 = Extension(id=3, name="pdf")

        session.add_all([extension1, extension2, extension3])
        session.commit()

        books = [
            Book(
                id=1,
                title="Преступление и наказание",
                year_written="1866",
                extensions=[extension1, extension2],
                book_locations=[
                    BookLocation(book_id=1, extension_id=1, location="1.epub"),
                    BookLocation(book_id=1, extension_id=2, location="1.fb2"),
                ]
            ),
            Book(
                id=2,
                title="Талисман",
                year_written="2005",
                extensions=[extension1, extension3],
                book_locations=[
                    BookLocation(book_id=1, extension_id=1, location="2.epub"),
                    BookLocation(book_id=1, extension_id=3, location="2.pdf"),
                ]
            ),
            Book(
                id=3,
                title="Война и мир",
                year_written="1869",
                extensions=[extension2],
                book_locations=[
                    BookLocation(book_id=1, extension_id=2, location="3.fb2"),
                ]
            ),
        ]
        session.add_all(books)
        session.commit()


@pytest.mark.parametrize(
    "book_id, expected_result",
    [
        (1, ["epub", "fb2"]),
        (2, ["epub", "pdf"]),
        (3, ["fb2"])
    ]
)
def test_get_book_extensions(book_id: int, expected_result: list[str]):
    url = f"{BACKEND_URL}/books/{book_id}/extensions"
    response = requests.get(url)

    assert response.status_code == 200
    data = response.json()
    extensions = [item["extension"]["name"] for item in data]
    assert extensions == expected_result
