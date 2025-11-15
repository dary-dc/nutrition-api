# The schemas.py file defines the data models (schemas) for the app using Pydantic.
# These classes act as blueprints (skeletons) that describe the structure, properties, and data types of the objects the app will handle — such as User, Food, and Meal.

# Each class represents a data contract between the backend and external layers (like API requests/responses).
# They ensure type validation, automatic data conversion, and serialization.

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# ---------- PERMISSION ----------
class PermissionBase(BaseModel):
    name: str
    description: str | None

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: int


# ---------- ROLE ----------
class RoleBase(BaseModel):
    name: str
    description: str | None
    permissions: List[PermissionResponse]

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int


# ---------- USER ----------
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    role_ids: Optional[List[int]] = None  # allow admin to assign roles


class UserUpdate(UserBase):
    password: Optional[str] = None
    role_ids: Optional[List[int]] = None  # allow admin to change roles


class UserPartialUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    role_ids: Optional[List[int]] = None  # allow admin to change roles


class UserResponse(UserBase):
    id: int
    roles: List[RoleResponse]

    class Config:
        from_attributes = True


# ---------- FOOD ----------
class FoodBase(BaseModel):
    name: str
    calories: float
    protein: float
    carbohydrates: float
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


class FoodResponse(FoodBase):
    id: int

    class Config:
        from_attributes = True


# ---------- MEAL ----------
class MealBase(BaseModel):
    id: int
    user_id: int
    name: str = Field(..., min_length=1, max_length=100)
    timestamp: Optional[datetime] = Field(
        None, description="Datetime of the meal (defaults to now on server)"
    )


class MealCreate(MealBase):
    # Must contain at least one food ID
    food_ids: List[int] = Field(
        ..., min_items=1, description="IDs of foods in this meal"
    )


class MealUpdate(BaseModel):
    food_ids: List[int] = Field(
        ..., min_items=1, description="IDs of foods in this meal"
    )


class MealPartialUpdate(BaseModel):
    name: Optional[str] = None
    timestamp: Optional[datetime] = None
    food_ids: Optional[List[int]] = None


class MealResponse(BaseModel):
    id: int
    name: str
    timestamp: datetime
    user_id: int
    foods: List["FoodResponse"]

    model_config = ConfigDict(from_attributes=True)
