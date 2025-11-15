# app/core/auth.py
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.exceptions import CredentialsException
from app.core.config import settings
from app.core.context import current_user_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v0/auth/login")

# ---------------- Get current user ----------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise CredentialsException()
    except JWTError:
        raise CredentialsException()

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise CredentialsException()

    # update context
    current_user_id.set(user.id)

    return user
