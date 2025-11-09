from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.const.base_roles import BASE_ROLES
from app.database import get_db
from app.core import security, auth
from app.exceptions import (
    UserAlreadyExistsException,
    InvalidLoginException,
)

router = APIRouter()


# ---------------- Register ----------------
@router.post("/register", response_model=schemas.UserResponse)
# TODO: add limit 5/min
def register(
    request: Request,
    new_user: schemas.UserCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(security.require_role(BASE_ROLES.ADMIN)),
):
    if db.query(models.User).filter(models.User.email == new_user.email).first():
        raise UserAlreadyExistsException()

    hashed_pw = security.get_password_hash(new_user.password)

    default_role = db.query(models.Role).filter_by(name=BASE_ROLES.USER).first()
    if not default_role:
        # If not seeded yet, raise a controlled error
        raise Exception("Default USER role not found. Run role seeding first.")

    db_user = models.User(
        username=new_user.username,
        email=new_user.email,
        hashed_password=hashed_pw,
        roles=[default_role],
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# ---------------- Login ----------------
@router.post("/login")
# TODO: add limit 5/min
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User).filter(models.User.username == form_data.username).first()
    )

    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise InvalidLoginException()

    access_token = security.create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


# ---------------- Current user ----------------
# Depends(get_current_user) does more than just injecting a value — it triggers
# FastAPI’s full dependency resolution chain (including nested deps like Session),
# along with yield cleanup, async handling, and overrides.
@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
