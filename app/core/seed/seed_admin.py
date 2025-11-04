from app.core.const.base_roles import BASE_ROLES
from app.models import Role, User
from app.core import security
from sqlalchemy.orm import Session


class MissingAdminRoleException(Exception):
    """Raised when the admin role has not been seeded yet."""
    pass


def seed_admin(db: Session):
    admin_role = db.query(Role).filter_by(name=BASE_ROLES.ADMIN).first()

    if not admin_role:
        raise MissingAdminRoleException(
            f"The required role '{BASE_ROLES.ADMIN}' was not found. "
            "Please run `seed_roles_and_permissions(db)` before seeding the admin user."
        )

    admin_user = db.query(User).filter_by(email="admin@system.local").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@system.local",
            hashed_password=security.get_password_hash("ChangeMe123!"),
            roles=[admin_role],
        )
        db.add(admin_user)
        db.commit()
