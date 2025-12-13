from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate

router = APIRouter(prefix="/auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def login_or_register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        if existing_user.password == user.password:
            return {"status": "ok", "action": "login", "user_id": existing_user.id}
        else:
            raise HTTPException(status_code=400, detail="Неверный пароль")
    else:
        new_user = User(username=user.username, password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"status": "ok", "action": "register", "user_id": new_user.id}
