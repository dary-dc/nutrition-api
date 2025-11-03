from fastapi import APIRouter, Depends, HTTPException
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
    db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)
):

    meals = db.query(models.Meal).filter(models.Meal.user_id == user.id).all()

    return meals


# ---------- GET single meal ----------
@router.get("/{meal_id}", response_model=schemas.MealResponse)
def get_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
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


# ---------- DELETE meal ----------
@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    db.delete(meal)
    db.commit()
    return {"detail": "Meal deleted successfully"}
