"""Bounded course-assistant inputs and downloadable text artifacts."""

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class AssistantMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=16000)


class AssistantRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    course_id: str = Field(min_length=1, max_length=80)
    lesson_id: str | None = Field(default=None, max_length=20)
    message: str = Field(min_length=1, max_length=4000)
    mode: Literal["hint", "environment", "code"] = "hint"
    platform: Literal["macos", "windows", "linux"] = "macos"
    code: str | None = Field(default=None, max_length=20000)
    error: str | None = Field(default=None, max_length=4000)
    history: list[AssistantMessage] = Field(default_factory=list, max_length=10)

    @field_validator("message")
    @classmethod
    def meaningful_message(cls, value):
        if not value.strip():
            raise ValueError("Describe what you need help with.")
        return value.strip()

    @model_validator(mode="after")
    def history_budget(self):
        if sum(len(item.content) for item in self.history) > 60000:
            raise ValueError("Conversation context is too large. Start a new chat.")
        return self


class AssistantFile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    path: str = Field(min_length=1, max_length=160)
    language: str = Field(min_length=1, max_length=24)
    content: str = Field(min_length=1, max_length=20000)
    target: Literal["lesson", "local"]

    @field_validator("path")
    @classmethod
    def relative_path(cls, value):
        parts = value.split("/")
        if (
            not re.fullmatch(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*", value)
            or any(part in (".", "..") or part.endswith((".", " ")) for part in parts)
            or any(
                part.split(".")[0].upper()
                in {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
                for part in parts
            )
        ):
            raise ValueError("Files must use portable relative paths without traversal.")
        return value


class AssistantBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")
    files: list[AssistantFile] = Field(min_length=1, max_length=6)

    @field_validator("files")
    @classmethod
    def bounded_files(cls, files):
        paths = [file.path.casefold() for file in files]
        if len(paths) != len(set(paths)) or any(
            other.startswith(path + "/") for path in paths for other in paths
        ):
            raise ValueError("Generated file paths must be unique and cannot overlap directories.")
        if sum(len(file.content) for file in files) > 80000:
            raise ValueError("Generated files are too large.")
        return files


class AssistantReply(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(min_length=1, max_length=12000)
    files: list[AssistantFile] = Field(max_length=6)

    @field_validator("files")
    @classmethod
    def bounded_files(cls, files):
        return AssistantBundle.bounded_files(files)
