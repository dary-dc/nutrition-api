from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from app.database import Base  # use the same registry of database.py


# e.g., fruits, vegetables, grains, protein foods, and dairy
class FoodCategory(Base):
    __tablename__ = "food_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    foods = Mapped[List["Food"]] = relationship("Food", back_populates="category")

    def __repr__(self):
        return f"<FoodCategory(name={self.name}, description={self.description})>"

