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


class ResearchExperiment(SQLModel, table=True):
    """A registered research question: hypothesis, specification and write-up."""

    id: str = Field(primary_key=True)
    owner: str = Field(index=True)
    number: int
    title: str
    hypothesis: str
    hypothesis_registered_at: str
    spec: dict = Field(sa_column=Column(JSON, nullable=False))
    notebook: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ResearchRun(SQLModel, table=True):
    """One execution of an experiment's frozen specification, or a rerun of one."""

    id: str = Field(primary_key=True)
    experiment_id: str = Field(foreign_key="researchexperiment.id", index=True)
    owner: str = Field(index=True)
    number: int
    kind: str = "run"
    rerun_of: str | None = None
    status: str = "queued"
    stage: str | None = None
    progress: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    spec: dict = Field(sa_column=Column(JSON, nullable=False))
    provenance: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    results: dict | None = Field(default=None, sa_column=Column(JSON, nullable=True))
    summary: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    reproduction: dict | None = Field(default=None, sa_column=Column(JSON, nullable=True))
    error: str | None = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    started_at: str | None = None
    finished_at: str | None = None
    heartbeat_at: float = 0.0
    duration_ms: int | None = None


class StrategyVersion(SQLModel, table=True):
    """Content-addressed strategy source, numbered per owner and strategy name."""

    __table_args__ = (
        UniqueConstraint("owner", "name", "sha256"),
        UniqueConstraint("owner", "name", "version"),
    )
    id: str = Field(primary_key=True)
    owner: str = Field(index=True)
    name: str
    version: int
    sha256: str
    code: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DatasetVersion(SQLModel, table=True):
    """Content-addressed dataset: a new version whenever the same dataset's content changes."""

    __table_args__ = (UniqueConstraint("key", "sha256"), UniqueConstraint("key", "version"))
    id: str = Field(primary_key=True)
    key: str = Field(index=True)
    version: int
    sha256: str
    kind: str
    meta: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    quality: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
