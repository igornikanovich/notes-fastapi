from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NoteCreateSchema(BaseModel):
    content: str


class NoteDetailsSchema(NoteCreateSchema):
    id: UUID
    date_created: datetime
    date_updated: datetime | None
    views: int

    class Config:
        from_attributes = True
