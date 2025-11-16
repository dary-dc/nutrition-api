from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base  # use the same registry of database.py
from app.models.nutrient_category import NutrientCategory


class Nutrient(Base):
    __tablename__ = "nutrient"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    unit: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("nutrient_category.id"), nullable=False)

    category: Mapped["NutrientCategory"] = relationship("NutrientCategory", foreign_keys=[category_id], back_populates="nutrients")

    def __repr__(self):
        return f"<Nutrient(name={self.name}, unit={self.unit}, description={self.description})>"

