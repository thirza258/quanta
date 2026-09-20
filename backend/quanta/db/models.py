import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, UniqueConstraint
from sqlmodel import Field, SQLModel


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


class ExamSubmission(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    exam_id: str = Field(index=True)
    result: dict = Field(sa_column=Column(JSON, nullable=False))
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Certificate(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("user_id", "course_key"),)
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    course_key: str
    record: dict = Field(sa_column=Column(JSON, nullable=False))
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TradingRun(SQLModel, table=True):
    id: str = Field(primary_key=True)
    owner: str = Field(index=True)
    version: int = 0
    state: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TradingDataset(SQLModel, table=True):
    id: str = Field(primary_key=True)
    bars: list = Field(sa_column=Column(JSON, nullable=False))
