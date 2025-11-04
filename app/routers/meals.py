from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.core import auth
from app.exceptions import NotFoundException

router = APIRouter()


# ---------- GET all meals ----------
@router.get("/", response_model=List[schemas.MealResponse])
def get_meals(
    page: int = Query(None, ge=1),
    skip: int = Query(None, ge=0),
    limit: int = Query(10, le=100),  # limit capped at 100 for safety
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user),
):
    # Prioritize page if both provided
    if page is not None:
        skip = (page - 1) * limit
    elif skip is None:
        skip = 0

    meals = (
        db.query(models.Meal)
        .offset(skip)
        .limit(limit)
        .filter(models.Meal.user_id == user.id)
        .all()
    )

    return meals


# ---------- GET single meal ----------
@router.get("/{meal_id}", response_model=schemas.MealResponse)
def get_meal(meal_id: int, db: Session = Depends(get_db)):

    meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not meal:
        raise NotFoundException()

    return meal


# ---------- CREATE meal ----------
@router.post("/", response_model=schemas.MealResponse)
def create_meal(
    meal_data: schemas.MealCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user),
):
    # Validate that all food IDs exist
    foods = db.query(models.Food).filter(models.Food.id.in_(meal_data.food_ids)).all()
    if len(foods) != len(meal_data.food_ids):
        # TODO: check proper message passing
        raise NotFoundException(detail="One or more food IDs not found")

    # Create the Meal
    new_meal = models.Meal(name=meal_data.name, user_id=user.id)
    new_meal.foods = foods  # ORM auto-fills association table

    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)

    return new_meal


# ---------- UPDATE food ----------
@router.put("/{meal_id}", response_model=schemas.MealResponse)
def update_meal(
    meal_id: int,
    updated_meal: schemas.MealUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user),
):
    db_meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()

    if not db_meal:
        raise NotFoundException()

    for key, value in updated_meal.model_dump().items():
        setattr(db_meal, key, value)

    db.commit()
    db.refresh(db_meal)

    return db_meal


# ---------- PARTIAL UPDATE meal ----------
@router.patch("/{meal_id}", response_model=schemas.MealResponse)
def partial_update_meal(
    meal_id: int,
    partial_meal: schemas.MealPartialUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user),
):
    db_meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()

    if not db_meal:
        raise NotFoundException()

    # Only update provided fields (exclude_unset=True)
    for key, value in partial_meal.model_dump(exclude_unset=True).items():
        setattr(db_meal, key, value)

    db.commit()
    db.refresh(db_meal)
    return db_meal


# ---------- DELETE meal ----------
@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):

    meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not meal:
        raise NotFoundException()

    db.delete(meal)
    db.commit()
    return {"detail": "Meal deleted successfully"}
