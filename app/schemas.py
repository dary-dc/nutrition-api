# The schemas.py file defines the data models (schemas) for the app using Pydantic.
# These classes act as blueprints (skeletons) that describe the structure, properties, and data types of the objects the app will handle — such as User, Food, and Meal.

# Each class represents a data contract between the backend and external layers (like API requests/responses).
# They ensure type validation, automatic data conversion, and serialization.

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


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


class FoodUpdate(FoodBase):
    pass


class FoodPartialUpdate(BaseModel):
    name: Optional[str]
    calories: Optional[float]
    protein: Optional[float]
    fat: Optional[float]
    carbohydrates: Optional[float]


# TODO: check functioning and purpose of this
class FoodResponse(FoodBase):
    id: int

    class Config:
        from_attributes = True


# ---------- MEAL ----------
# ---------- Base (shared) ----------
class MealBase(BaseModel):
    id: int
    user_id: int
    name: str = Field(..., min_length=1, max_length=100)
    timestamp: Optional[datetime] = Field(
        None, description="Datetime of the meal (defaults to now on server)"
    )


# ---------- CREATE ----------
class MealCreate(MealBase):
    # Must contain at least one food ID
    food_ids: List[int] = Field(
        ..., min_items=1, description="IDs of foods in this meal"
    )


# ---------- UPDATE ----------
class MealUpdate(BaseModel):
    pass


# ---------- PARTIAL UPDATE (PATCH) ----------
class MealPartialUpdate(BaseModel):
    name: Optional[str] = None
    timestamp: Optional[datetime] = None
    food_ids: Optional[List[int]] = None


# ---------- RESPONSE ----------
class MealResponse(BaseModel):
    id: int
    name: str
    timestamp: datetime
    user_id: int
    foods: List["FoodResponse"]

    model_config = ConfigDict(from_attributes=True)
