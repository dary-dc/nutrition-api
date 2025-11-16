from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from app.database import Base  # use the same registry of database.py
from app.models.associations import user_role_association


class User(Base):
    __tablename__ = "user"

    # --- Basic mapped_columns ---
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    # --- Object references (linked models) ---
    # One-to-many: User → Meal
    meals: Mapped[List["Meal"]] = relationship(
        "Meal", back_populates="user", cascade="all, delete-orphan", foreign_keys="Meal.user_id",
    )

    # Many-to-many: User ↔ Role
    roles: Mapped[List["Role"]] = relationship(
        "Role", secondary=user_role_association, back_populates="users"
    )

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

    def has_role(self, role_name: str) -> bool:
        """Convenience helper: check if the user has a given role."""
        return any(role.name == role_name for role in self.roles)

    def has_permission(self, permission_name: str) -> bool:
        return any(permission_name == p.name for r in self.roles for p in r.permissions)
