# The models.py file defines the database structure using SQLAlchemy ORM.
# Each class represents a table in the database, and each attribute (column) represents a field in that table.

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base  # use the same registry of database.py
from typing import List


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


# ------------------------
# Models
# ------------------------


class Permission(Base):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    roles: Mapped[List["Role"]] = relationship(
        "Role", secondary=role_permission_association, back_populates="permissions"
    )

    def __repr__(self):
        return f"<Permission(name={self.name})>"


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    # Back reference to users (many-to-many)
    users: Mapped[List["User"]] = relationship(
        "User", secondary=user_role_association, back_populates="roles"
    )
    permissions: Mapped[List["Permission"]] = relationship(
        "Permission", secondary=role_permission_association, back_populates="roles"
    )

    def __repr__(self):
        return f"<Role(name={self.name})>"


class User(Base):
    __tablename__ = "user"

    # --- Basic columns ---
    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)

    # --- Object references (linked models) ---
    # One-to-many: User → Meal
    meals: Mapped[List["Meal"]] = relationship(
        "Meal", back_populates="user", cascade="all, delete-orphan", foreign_keys=lambda: [Meal.user_id],
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


class Meal(Base):
    __tablename__ = "meal"

    # --- Basic columns ---
    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("user.id"), nullable=False)
    name: str = Column(String(100), nullable=False)
    timestamp: DateTime = Column(
        DateTime(timezone=True), server_default=func.now()
    )  # generate datetime at the DB level

    # --- Object references (linked models) ---
    user: Mapped["User"] = relationship("User", back_populates="meals", foreign_keys=[user_id])
    foods: Mapped[List["Food"]] = relationship("Food", secondary=meal_food_association)

    def __repr__(self):
        return f"<Meal(name={self.name}, user_id={self.user_id}, timestamp={self.timestamp})>"
