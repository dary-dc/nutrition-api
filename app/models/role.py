from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.database import Base
from app.models.associations import user_role_association, role_permission_association

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
