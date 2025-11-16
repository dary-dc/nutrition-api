from datetime import datetime, timedelta, timezone
from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext
from app.core import auth
from app.core.config import settings
from app.exceptions import AccessException
from app.models.user import User

# Argon2 is modern, memory-hard, and recommended by OWASP for new systems.
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def require_permission(permission_name: str):
    def wrapper(user: User = Depends(auth.get_current_user)):
        if not user.has_permission(permission_name):
            raise AccessException(detail=f"User has no access to this resource")
        return user

    return wrapper


def require_role(role_name: str):
    def wrapper(user: User = Depends(auth.get_current_user)):
        if not user.has_role(role_name):
            raise AccessException(detail=f"User has no access to this resource")
        return user

    return wrapper
