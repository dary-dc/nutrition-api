from app.models import models
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.core.security import require_role, get_password_hash
from app.core.const.base_roles import BASE_ROLES
from app.database import get_db
from app.exceptions import NotFoundException, UserAlreadyExistsException

router = APIRouter()


# ---------- GET all users (with pagination) ----------
@router.get("/", response_model=List[schemas.UserResponse])
def get_users(
    page: int = Query(None, ge=1),
    skip: int = Query(None, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(require_role(BASE_ROLES.ADMIN)),
):
    if page is not None:
        skip = (page - 1) * limit
    elif skip is None:
        skip = 0

    users = (
        db.query(models.User)
        .order_by(models.User.id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return users


# ---------- GET user by ID ----------
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(require_role(BASE_ROLES.ADMIN)),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise NotFoundException()

    return db_user


# ---------- CREATE new user ----------
@router.post(
    "/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(require_role(BASE_ROLES.ADMIN)),
):
    # Check duplicates
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise UserAlreadyExistsException()

    # Hash password
    hashed_pw = get_password_hash(user_in.password)

    new_user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pw,
    )
    print(db.query(models.Role).filter(models.Role.id.in_(user_in.role_ids)).all())
    # Assign roles if provided
    if user_in.role_ids:
        roles = db.query(models.Role).filter(models.Role.id.in_(user_in.role_ids)).all()
    else:
        default_role = db.query(models.Role).filter_by(name=BASE_ROLES.USER).first()
        if not default_role:
            raise Exception("Default USER role not found. Run seed_roles().")
        roles = [default_role]

    new_user.roles = roles

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ---------- UPDATE user ----------
@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: schemas.UserCreate,  # full update: must include password, etc.
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(require_role(BASE_ROLES.ADMIN)),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise NotFoundException()

    for key, value in user_update.model_dump().items():
        if key == "password":
            setattr(db_user, "hashed_password", get_password_hash(value))
        elif hasattr(db_user, key):
            setattr(db_user, key, value)

    if user_update.role_ids is not None:
        new_roles = (
            db.query(models.Role).filter(models.Role.id.in_(user_update.role_ids)).all()
        )
        db_user.roles = new_roles

    db.commit()
    db.refresh(db_user)
    return db_user


# ---------- PARTIAL UPDATE user ----------
@router.patch("/{user_id}", response_model=schemas.UserResponse)
def partial_update_user(
    user_id: int,
    user_update: schemas.UserBase,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(require_role(BASE_ROLES.ADMIN)),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise NotFoundException()

    for key, value in user_update.model_dump(exclude_unset=True).items():
        if key == "password":
            setattr(db_user, "hashed_password", get_password_hash(value))
        elif hasattr(db_user, key):
            setattr(db_user, key, value)

    if user_update.role_ids is not None:
        new_roles = (
            db.query(models.Role).filter(models.Role.id.in_(user_update.role_ids)).all()
        )
        db_user.roles = new_roles

    db.commit()
    db.refresh(db_user)
    return db_user


# ---------- DELETE user ----------
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(require_role(BASE_ROLES.ADMIN)),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise NotFoundException()

    db.delete(db_user)
    db.commit()
    return
