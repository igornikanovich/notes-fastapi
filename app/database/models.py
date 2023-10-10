import datetime
from uuid import uuid4

from sqlalchemy import Column, UUID, DateTime, String, Integer

from app.database.setup import Base


class Note(Base):
    __tablename__ = 'notes'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    date_created = Column(DateTime(), nullable=False, default=datetime.datetime.now)
    date_updated = Column(DateTime(), onupdate=datetime.datetime.now)
    content = Column(String)
    views = Column(Integer, default=0)
