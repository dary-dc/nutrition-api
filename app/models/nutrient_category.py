from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from app.database import Base  # use the same registry of database.py
from app.models.nutrient import Nutrient

# e.g., macronutrients (carbohydrates, proteins, fats, and water) and micronutrients (vitamins and minerals)
class NutrientCategory(Base):
    __tablename__ = "nutrient_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    nutrients: Mapped[List["Nutrient"]] = relationship("Nutrient", back_populates="category")

