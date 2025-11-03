# The models.py file defines the database structure using SQLAlchemy ORM.
# Each class represents a table in the database, and each attribute (column) represents a field in that table.

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, Mapped
from app.database import Base  # use the same registry of database.py
from sqlalchemy.sql import func
from typing import List


class Food(Base):
    __tablename__ = "food"

    # --- Basic columns ---
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, nullable=False)
    calories: float = Column(Float, nullable=False)
    protein: float = Column(Float, nullable=False)
    fat: float = Column(Float, nullable=False)
    carbohydrates: float = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Food(name={self.name}, calories={self.calories})>"


class User(Base):
    __tablename__ = "user"

    # --- Basic columns ---
    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)

    # --- Object references (linked models) ---
    meals: Mapped[List["Meal"]] = relationship(
        "Meal", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


# Association table for many-to-many relationship between Meal and Foods
meal_food_association = Table(
    "meal_food_association",
    Base.metadata,
    # PK avoids duplicates and makes joins faster
    Column("meal_id", Integer, ForeignKey("meal.id"), primary_key=True),
    Column("food_id", Integer, ForeignKey("food.id"), primary_key=True),
)


class Meal(Base):
    __tablename__ = "meal"

    # --- Basic columns ---
    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("user.id"), nullable=False)
    name: str = Column(String, nullable=False)
    timestamp: DateTime = Column(
        DateTime(timezone=True), server_default=func.now()
    ) # generate datetime at the DB level

    # --- Object references (linked models) ---
    user: Mapped["User"] = relationship("User", back_populates="meals")
    foods: Mapped[List["Food"]] = relationship("Food", secondary=meal_food_association)

    def __repr__(self):
        return f"<Meal(name={self.name}, user_id={self.user_id}, timestamp={self.timestamp})>"
