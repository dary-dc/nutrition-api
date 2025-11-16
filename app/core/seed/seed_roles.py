from app.core.const.base_roles import BASE_ROLES
from app.models.role import Role
from app.models.permission import Permission
from sqlalchemy.orm import Session


def seed_roles(db: Session):

    # Create base roles and assign permissions
    admin = db.query(Role).filter_by(name=BASE_ROLES.ADMIN).first()
    if not admin:
        admin = Role(name=BASE_ROLES.ADMIN, description="System administrator")
        admin.permissions = db.query(Permission).all()
        db.add(admin)

    specialist = db.query(Role).filter_by(name=BASE_ROLES.SPECIALIST).first()
    if not specialist:
        specialist = Role(name=BASE_ROLES.SPECIALIST, description="Nutrition expert")
        specialist.permissions = [
            p
            for p in db.query(Permission).all()
            if p.name.startswith("meal.") or p.name.startswith("food.")
        ]
        db.add(specialist)

    db.commit()
