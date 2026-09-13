import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import JSON, Column
from sqlmodel import Field, Session, SQLModel, create_engine

STORAGE = Path(os.getenv("QUANTA_STORAGE", str(Path(__file__).resolve().parents[1] / "storage")))
STORAGE.mkdir(parents=True, exist_ok=True)
url = os.getenv("DATABASE_URL", f"sqlite:///{STORAGE}/quanta.db")
engine = create_engine(
    url,
    connect_args={"check_same_thread": False} if url.startswith("sqlite") else {},
    pool_pre_ping=True,
)


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    hashed_password: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AuthSession(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    expires_at: int


class Workspace(SQLModel, table=True):
    user_id: str = Field(foreign_key="user.id", primary_key=True)
    version: int = 0
    state: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Submission(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    lesson_id: str
    answer: int
    correct: bool
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def get_session():
    with Session(engine) as session:
        yield session


def initialize():
    SQLModel.metadata.create_all(engine)
