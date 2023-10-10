from typing import Sequence
from uuid import UUID

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from app.database.crud import NotesCRUD
from app.database.models import Note
from app.database.setup import engine, Base, get_session
from app.schemas.note import NoteDetailsSchema, NoteCreateSchema

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


db = NotesCRUD()


@app.get('/notes/', response_model=list[NoteDetailsSchema])
async def get_all_notes(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)) -> Sequence[Note]:
    return await db.get_all(session=session, skip=skip, limit=limit)


@app.post('/notes/', response_model=NoteDetailsSchema, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreateSchema, session: AsyncSession = Depends(get_session)) -> Note:
    return await db.create(session=session, data=note)


@app.get('/notes/{note_id}', response_model=NoteDetailsSchema)
async def get_note_by_id(note_id: UUID, session: AsyncSession = Depends(get_session)) -> Note:
    return await db.get_with_increase_views(session=session, note_id=note_id)


@app.patch('/notes/{note_id}', response_model=NoteDetailsSchema)
async def update_note(note_id: UUID, data: NoteCreateSchema, session: AsyncSession = Depends(get_session)) -> Note:
    return await db.update(session=session, note_id=note_id, data=data)


@app.delete('/notes/{note_id}', response_model=NoteDetailsSchema)
async def delete_note(note_id: UUID, session: AsyncSession = Depends(get_session)) -> Response:
    await db.delete(session=session, note_id=note_id)
    return Response(status_code=204)
