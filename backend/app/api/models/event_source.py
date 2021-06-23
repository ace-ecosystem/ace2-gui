from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from api.models import type_str, validators


class EventSourceBase(BaseModel):
    """Represents a source that can be applied to an event (phishing, host compromise, etc)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the event source")

    uuid: Optional[UUID] = Field(description="The UUID of the event source")

    value: type_str = Field(description="The value of the event source")

    _prevent_none: classmethod = validators.prevent_none("uuid", "value")


class EventSourceCreate(EventSourceBase):
    pass


class EventSourceRead(EventSourceBase):
    uuid: UUID = Field(description="The UUID of the event source")

    class Config:
        orm_mode = True


class EventSourceUpdate(EventSourceBase):
    value: Optional[type_str] = Field(description="The value of the event source")
