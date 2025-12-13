from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Note
from schemas import NoteCreate, NoteOut

router = APIRouter(prefix="/notes")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=NoteOut)
def create_note(note: NoteCreate, user_id: int, db: Session = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content, user_id=user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/", response_model=list[NoteOut])
def get_notes(user_id: int, db: Session = Depends(get_db)):
    return db.query(Note).filter(Note.user_id == user_id).all()

@router.delete("/{note_id}/{user_id}")
def delete_note(
    note_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"status": "ok", "message": "Note deleted"}