# The models.py file defines the database structure using SQLAlchemy ORM.
# Each class represents a table in the database, and each attribute (column) represents a field in that table.

from sqlalchemy import Column
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Food(Base):
    __tablename__ = 'food_items'

    # --- Basic columns ---
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    carbohydrates = Column(Float, nullable=False)

    def __repr__(self):
        return f"<FoodItem(name={self.name}, calories={self.calories})>"

class User(Base):
    __tablename__ = 'users'

    # --- Basic columns ---
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # --- Object references (linked models) ---
    meals = relationship("Meal", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

# Association table for many-to-many relationship between Meal and FoodItem
meal_food_association = Table(
    'meal_food_association',
    Base.metadata,
    Column('meal_id', Integer, ForeignKey('meals.id')),
    Column('food_item_id', Integer, ForeignKey('food_items.id'))
)

class Meal(Base):
    __tablename__ = 'meals'

    # --- Basic columns ---
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # --- Object references (linked models) ---
    user = relationship("User", back_populates="meals")
    food_items = relationship("FoodItem", secondary=meal_food_association, backref="meals")

    def __repr__(self):
        return f"<Meal(name={self.name}, user_id={self.user_id}, timestamp={self.timestamp})>"