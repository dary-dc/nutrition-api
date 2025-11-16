from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base  # use the same registry of database.py


class FoodMeasure(Base):
    __tablename__ = "food_measure"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    food_id: Mapped[int] = mapped_column(Integer, ForeignKey("food.id"), nullable=False)
    gram_weight: float = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True) # (e.g., "1 cup", "1 egg", "1 serving", "100 ml")

    food: Mapped["Food"] = relationship("Food", foreign_keys=[food_id], back_populates="food_measures")

    def __repr__(self):
        return f"<FoodMeasure(name={self.food_id}, weight_in_grams={self.gram_weight}, description={self.description})>"

