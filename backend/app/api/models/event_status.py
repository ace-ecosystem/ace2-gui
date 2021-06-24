from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

from api.models import type_str, validators


class EventStatusBase(BaseModel):
    """Represents a status that can be applied to an event (open, closed, etc)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the event status")

    uuid: UUID = Field(default_factory=uuid4, description="The UUID of the event status")

    value: type_str = Field(description="The value of the event status")


class EventStatusCreate(EventStatusBase):
    pass


class EventStatusRead(EventStatusBase):
    class Config:
        orm_mode = True


class EventStatusUpdate(EventStatusBase):
    value: Optional[type_str] = Field(description="The value of the event status")

    _prevent_none: classmethod = validators.prevent_none("value")
