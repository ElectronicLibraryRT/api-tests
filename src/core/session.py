from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.settings import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB
)


DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

session_maker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)