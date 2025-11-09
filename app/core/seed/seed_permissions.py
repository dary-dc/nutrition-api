from app.core.const.permissions import PERMISSIONS
from app.models import Permission
from sqlalchemy.orm import Session


def seed_permissions(db: Session):

    # Ensure all permissions exist
    existing = {p.name for p in db.query(Permission).all()}
    for perm_name in PERMISSIONS.ALL:
        if perm_name not in existing:
            db.add(Permission(name=perm_name))

    db.commit()
