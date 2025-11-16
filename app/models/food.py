from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from app.database import Base  # use the same registry of database.py
from app.models.nutrient import Nutrient
from app.models.food_category import FoodCategory
from app.models.food_measure import FoodMeasure
from app.models.associations import food_nutrient_association


class Food(Base):
    __tablename__ = "food"

    # --- Basic mapped_columns ---
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    calories_per_100g: float = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    brand: Mapped[str] = mapped_column(String, nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("food_category.id"), nullable=False)

    category: Mapped["FoodCategory"] = relationship("FoodCategory", foreign_keys=[category_id], back_populates="foods")
    nutrients: Mapped[List["Nutrient"]] = relationship("Nutrient", secondary=food_nutrient_association)
    food_measures: Mapped[List["FoodMeasure"]] = relationship("FoodMeasure", back_populates="food")

    def __repr__(self):
        return f"<Food(name={self.name}, calories_per_100g={self.calories_per_100g}, nutrients=[{', '.join(map(lambda n: n.name,  self.nutrients))}])>"
