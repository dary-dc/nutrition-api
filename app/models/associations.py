from sqlalchemy import Column, Integer, Float, ForeignKey, Table
from app.database import Base  # use the same registry of database.py

# ------------------------
# Association Tables
# ------------------------


# Many-to-many: Meal ↔ Food
meal_food_association = Table(
    "meal_food_association",
    Base.metadata,
    # PK avoids duplicates and makes joins faster
    Column("meal_id", Integer, ForeignKey("meal.id"), primary_key=True),
    Column("food_id", Integer, ForeignKey("food.id"), primary_key=True),
)


# Many-to-many: User ↔ Role
user_role_association = Table(
    "user_role_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
)


# one-to-many: Role ↔ Permission
role_permission_association = Table(
    "role_permission_association",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permission.id"), primary_key=True),
)


food_nutrient_association = Table(
    "food_nutrient",
    Base.metadata,
    Column("food_id", Integer, ForeignKey("food.id"), primary_key=True),
    Column("nutrient_id", Integer, ForeignKey("nutrient.id"), primary_key=True),
    Column("value_per_100g", Float, nullable=False),
    Column("source_id", Integer, ForeignKey("source.id"))
)
