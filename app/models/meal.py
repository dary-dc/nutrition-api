from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from app.database import Base  # use the same registry of database.py
from app.models.associations import meal_food_association
from app.models.user import User
from app.models.food import Food


class Meal(Base):
    __tablename__ = "meal"

    # --- Basic mapped_columns ---
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    timestamp: DateTime = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )  # generate datetime at the DB level

    # --- Object references (linked models) ---
    user: Mapped["User"] = relationship("User", back_populates="meals", foreign_keys=[user_id])
    foods: Mapped[List["Food"]] = relationship("Food", secondary=meal_food_association)

    def __repr__(self):
        return f"<Meal(name={self.name}, user_id={self.user_id}, timestamp={self.timestamp})>"
