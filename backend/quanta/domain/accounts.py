from __future__ import annotations

from typing import Any

from pydantic import BaseModel, EmailStr, Field


class Credentials(BaseModel):
    email: EmailStr = Field(max_length=254)
    password: str = Field(min_length=10, max_length=128)
    name: str = Field("Researcher", min_length=1, max_length=60)


class WorkspacePayload(BaseModel):
    version: int = Field(ge=0)
    state: dict[str, Any]
