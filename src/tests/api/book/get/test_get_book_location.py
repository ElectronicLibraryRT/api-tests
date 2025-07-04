import hashlib
import os
import boto3
from botocore.client import Config
import pytest
import requests
from src.core.models import Book, Extension, Author, Genre, BookLocation
from src.core.models.base import Base
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
        author1 = Author(id=1, name="Рэй Брэдбери")
        author2 = Author(id=2, name="Джон Толкин")
        author3 = Author(id=3, name="Айзек Азимов")
        author4 = Author(id=4, name="Фёдор Достоевский")

        session.add_all([author1, author2, author3, author4])
        session.commit()

        genre1 = Genre(id=1, name="Антиутопия")
        genre2 = Genre(id=2, name="Фэнтези")
        genre3 = Genre(id=3, name="Фантастика")
        genre4 = Genre(id=4, name="Драма")

        session.add_all([genre1, genre2, genre3, genre4])
        session.commit()

        extension1 = Extension(id=1, name="pdf")
        extension2 = Extension(id=2, name="fb2")
        extension3 = Extension(id=3, name="epub")

        session.add_all([extension1, extension2, extension3])
        session.commit()

        books = [
            Book(
                id=1,
                title="451 градус по Фаренгейту",
                year_written=1953,
                authors=[author1],
                genres=[genre1],
                extensions=[extension1, extension2],
                book_locations=[
                    BookLocation(book_id=1, extension_id=1, location="1.pdf"),
                    BookLocation(book_id=1, extension_id=2, location="1.fb2"),
                ]
            ),
            Book(
                id=2,
                title="Хоббит, или Туда и обратно",
                year_written=1937,
                authors=[author2],
                genres=[genre2],
                extensions=[extension3],
                book_locations=[
                    BookLocation(book_id=2, extension_id=3, location="2.epub"),
                ]
            ),
            Book(
                id=3,
                title="Основание",
                year_written=1942,
                authors=[author3],
                genres=[genre3],
                extensions=[extension2],
                book_locations=[
                    BookLocation(book_id=3, extension_id=2, location="3.fb2"),
                ]
            ),
            Book(
                id=4,
                title="Преступление и наказание",
                year_written=1866,
                authors=[author4],
                genres=[genre4],
                extensions=[extension3],
                book_locations=[
                    BookLocation(book_id=4, extension_id=3, location="4.epub"),
                ]
            ),
        ]
        session.add_all(books)
        session.commit()


@pytest.mark.parametrize(
    "book_id, extension_id, file_name",
    [
        (1, 1, "1.pdf"),
        (1, 2, "1.fb2"),
        (2, 3, "2.epub"),
        (3, 2, "3.fb2"),
        (4, 3, "4.epub"),
    ]
)
def test_get_book_extensions(book_id: int, extension_id: int, file_name: str):
    local_path = os.path.join(FILES_DIR, file_name)

    url = f"{BACKEND_URL}/books/{book_id}/extensions/{extension_id}"
    response = requests.get(url)

    assert response.status_code == 200
    data = response.json()
    file_url = f"http://{MINIO_HOST}:{MINIO_PORT}{data['location']}"

    download_response = requests.get(file_url)
    assert download_response.status_code == 200

    with open(local_path, 'rb') as f:
        local_bytes = f.read()

    downloaded_hash = hashlib.sha256(download_response.content).hexdigest()
    local_hash = hashlib.sha256(local_bytes).hexdigest()
    assert downloaded_hash == local_hash
