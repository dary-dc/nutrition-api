from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import SessionLocal, get_db
from app.core import auth

router = APIRouter()

# ---------- CREATE meal ----------
@router.post("/", response_model=schemas.MealResponse)
def create_meal(meal: schemas.MealCreate, db: Session = Depends(get_db)):
    # Assume current_user_id = 1 for now (auth not implemented yet)
    user_id = 1
    db_meal = models.Meal(user_id=user_id)
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)

    # Add foods to meal
    for food_entry in meal.foods:
        db_meal_food = models.MealFood(
            meal_id=db_meal.id,
            food_id=food_entry.food_id,
            quantity=food_entry.quantity
        )
        db.add(db_meal_food)
    db.commit()
    db.refresh(db_meal)
    return db_meal


# ---------- GET all meals ----------
@router.get("/", response_model=List[schemas.MealResponse])
def get_meals(db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):

    meals = db.query(models.Meal).filter(models.Meal.user_id == user.id).all()

    return meals


# ---------- GET single meal ----------
@router.get("/{meal_id}", response_model=schemas.MealResponse)
def get_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


# ---------- DELETE meal ----------
@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    db.delete(meal)
    db.commit()
    return {"detail": "Meal deleted successfully"}
