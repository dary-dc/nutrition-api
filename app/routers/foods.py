from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.exceptions import AccessException, NotFoundException
from app.core import auth

router = APIRouter()

# ---------- GET all foods (with pagination) ----------
@router.get("/", response_model=List[schemas.FoodResponse])
def get_foods(
    page: int = Query(None, ge=1),
    skip: int = Query(None, ge=0),
    limit: int = Query(10, le=100),  # limit capped at 100 for safety
    db: Session = Depends(get_db)
):
    # Prioritize page if both provided
    if page is not None:
        skip = (page - 1) * limit
    elif skip is None:
        skip = 0

    foods = db.query(models.Food).offset(skip).limit(limit).all()
    return foods


# ---------- GET food by ID ----------
@router.get("/{food_id}", response_model=schemas.FoodResponse)
def get_food(food_id: int, db: Session = Depends(get_db)):

    food = db.query(models.Food).filter(models.Food.id == food_id).first()

    if not food:
        raise NotFoundException()

    return food


# ---------- CREATE new food ----------
@router.post("/", response_model=schemas.FoodResponse)
def create_food(food: schemas.FoodCreate, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):

    if not user.is_admin or not user.is_specialist:
        raise AccessException()

    db_food = models.Food(**food.model_dump())

    db.add(db_food)
    db.commit()
    db.refresh(db_food)

    return db_food


# ---------- UPDATE food ----------
@router.put("/{food_id}", response_model=schemas.FoodResponse)
def update_food(food_id: int, updated_food: schemas.FoodCreate, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):

    if not user.is_admin or not user.is_specialist:
        raise AccessException()

    db_food = db.query(models.Food).filter(models.Food.id == food_id).first()

    if not db_food:
        raise NotFoundException()

    for key, value in updated_food.model_dump().items():
        setattr(db_food, key, value)

    db.commit()
    db.refresh(db_food)

    return db_food


# ---------- DELETE food ----------
@router.delete("/{food_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_food(food_id: int, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):

    if not user.is_admin:
        raise AccessException()

    food = db.query(models.Food).filter(models.Food.id == food_id).first()

    if not food:
        raise NotFoundException()

    db.delete(food)
    db.commit()

    return None
