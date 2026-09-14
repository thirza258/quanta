"""Engine and session lifecycle; SQLModel tables are registered by models."""

import os

from sqlmodel import Session, SQLModel, create_engine

from quanta.core.config import STORAGE
from quanta.db import models  # noqa: F401

url = os.getenv("DATABASE_URL", f"sqlite:///{STORAGE}/quanta.db")
engine = create_engine(
    url,
    connect_args={"check_same_thread": False} if url.startswith("sqlite") else {},
    pool_pre_ping=True,
)


def get_session():
    with Session(engine) as session:
        yield session


def initialize():
    SQLModel.metadata.create_all(engine)
