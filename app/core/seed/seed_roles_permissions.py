from app.core.const.base_roles import BASE_ROLES
from app.core.const.permissions import PERMISSIONS
from app.models import Role, Permission
from sqlalchemy.orm import Session


def seed_roles_and_permissions(db: Session):

    # Ensure all permissions exist
    existing = {p.name for p in db.query(Permission).all()}
    for perm_name in PERMISSIONS.ALL:
        if perm_name not in existing:
            db.add(Permission(name=perm_name))
    db.flush()  # ensures new permissions are available before roles

    # Create base roles and assign permissions
    admin = db.query(Role).filter_by(name=BASE_ROLES.ADMIN).first()
    if not admin:
        admin = Role(name=BASE_ROLES.ADMIN)
        admin.permissions = db.query(Permission).all()
        db.add(admin)

    specialist = db.query(Role).filter_by(name=BASE_ROLES.SPECIALIST).first()
    if not specialist:
        specialist = Role(name=BASE_ROLES.SPECIALIST)
        specialist.permissions = [
            p
            for p in db.query(Permission).all()
            if p.name.startswith("meal.") or p.name.startswith("food.")
        ]
        db.add(specialist)

    db.commit()
