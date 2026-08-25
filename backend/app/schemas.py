from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    key: str = Field(min_length=2, max_length=80, pattern=r"^[a-z0-9_-]+$")
    name: str = Field(min_length=1, max_length=160)
    description: str = ""


class ProjectRead(ProjectCreate):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class EnvironmentCreate(BaseModel):
    key: str = Field(min_length=2, max_length=80, pattern=r"^[a-z0-9_-]+$")
    name: str = Field(min_length=1, max_length=160)


class EnvironmentRead(EnvironmentCreate):
    id: int
    project_id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class TargetingRule(BaseModel):
    attribute: str = Field(min_length=1, max_length=100)
    operator: Literal["equals", "not_equals", "in", "not_in", "contains"]
    value: Any


class FlagCreate(BaseModel):
    key: str = Field(min_length=2, max_length=120, pattern=r"^[a-z0-9_-]+$")
    name: str = Field(min_length=1, max_length=160)
    description: str = ""
    enabled: bool = False
    premium_only: bool = False
    rollout_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    targeting_rules: list[TargetingRule] = Field(default_factory=list)


class FlagUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = None
    enabled: bool | None = None
    premium_only: bool | None = None
    rollout_percentage: float | None = Field(default=None, ge=0.0, le=100.0)
    targeting_rules: list[TargetingRule] | None = None


class FlagRead(BaseModel):
    id: int
    environment_id: int
    key: str
    name: str
    description: str
    enabled: bool
    premium_only: bool
    rollout_percentage: float
    targeting_rules: list[dict]
    version: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class UserContext(BaseModel):
    id: str = Field(min_length=1, max_length=200)
    premium: bool = False
    attributes: dict[str, Any] = Field(default_factory=dict)


class EvaluationRequest(BaseModel):
    project_key: str
    environment_key: str
    flag_key: str
    user: UserContext


class EvaluationResponse(BaseModel):
    flag_key: str
    enabled: bool
    reason: str
    bucket: int | None = None
    rollout_percentage: float | None = None


class AuditRead(BaseModel):
    id: int
    actor: str
    action: str
    entity_type: str
    entity_id: str
    payload: dict
    created_at: datetime
    model_config = {"from_attributes": True}
