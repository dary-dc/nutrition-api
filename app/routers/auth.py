from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.core import security, auth
from app.exceptions import (
    UserAlreadyExistsException,
    InvalidLoginException,
)
from core.limiter import limiter

router = APIRouter()


# ---------------- Register ----------------
@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    if db.query(models.User).filter(models.User.email == user.email).first():
        raise UserAlreadyExistsException()

    hashed_pw = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, password_hash=hashed_pw)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# ---------------- Login ----------------
@router.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise InvalidLoginException()

    access_token = security.create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


# Depends(get_current_user) does more than just injecting a value — it triggers
# FastAPI’s full dependency resolution chain (including nested deps like Session),
# along with yield cleanup, async handling, and overrides.
@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
