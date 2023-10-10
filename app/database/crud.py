from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Note
from app.schemas.note import NoteCreateSchema


class NotesCRUD:
    async def create(self, session: AsyncSession, data: NoteCreateSchema) -> Note:
        instance = Note(content=data.content)

        session.add(instance=instance)
        await session.commit()
        await session.refresh(instance=instance)

        return instance

    async def get(self, session: AsyncSession, note_id: str | UUID) -> Note:
        statement = select(Note).filter(Note.id == note_id)
        result = await session.execute(statement=statement)
        note = result.scalar_one_or_none()

        if note is None:
            raise HTTPException(status_code=404, detail='Note does not exist')

        return note

    async def update(self, session: AsyncSession, note_id: str | UUID, data: NoteCreateSchema) -> Note:
        note = await self.get(session=session, note_id=note_id)

        note.content = data.content

        session.add(note)
        await session.commit()
        await session.refresh(instance=note)

        return note

    async def delete(self, session: AsyncSession, note_id: str | UUID) -> None:
        note = await self.get(session=session, note_id=note_id)

        await session.delete(instance=note)
        await session.commit()

    async def get_all(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Note]:
        statement = select(Note).offset(skip).limit(limit)
        result = await session.execute(statement=statement)

        return result.scalars().all()

    async def get_with_increase_views(self, session: AsyncSession, note_id: str | UUID) -> Note:
        note = await self.get(session=session, note_id=note_id)

        note.views += 1

        session.add(instance=note)
        await session.commit()
        await session.refresh(instance=note)

        return note
