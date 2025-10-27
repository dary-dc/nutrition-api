# The schemas.py file defines the data models (schemas) for the app using Pydantic.
# These classes act as blueprints (skeletons) that describe the structure, properties, and data types of the objects the app will handle — such as User, Food, and Meal.

# Each class represents a data contract between the backend and external layers (like API requests/responses).
# They ensure type validation, automatic data conversion, and serialization.

from pydantic import BaseModel
from typing import List, Optional
import datetime

# ---------- USER ----------
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True


# ---------- FOOD ----------
class FoodBase(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float

class FoodCreate(FoodBase):
    pass

class FoodResponse(FoodBase):
    id: int
    class Config:
        from_attributes = True


# ---------- MEAL ----------
class MealFoodBase(BaseModel):
    food_id: int
    quantity: float

class MealBase(BaseModel):
    date: Optional[datetime.datetime] = datetime.datetime.utcnow()

class MealCreate(MealBase):
    foods: List[MealFoodBase]

class MealResponse(MealBase):
    id: int
    user_id: int
    foods: List[MealFoodBase]
    class Config:
        from_attributes = True
