# -*- coding: utf-8 -*-
'''Get JWT tokens and hash the password.'''

from typing import Union
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core.config import SECRET_KEY
from custom_exceptions.exceptions import TOKEN_ERROR, INACTIVE_USER_ERROR
from models import auth, users
from db.database import get_db
from db import crud



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, email: EmailStr):
    user = crud.UserCrud.get_by_email(db, email)
    if user:
        user_dict = user.__dict__.copy()
        user_dict.pop('_sa_instance_state')

        return users.User(**user_dict)


def authenticate_user(db: Session, email: EmailStr, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


async def save_user(db: Session, user: users.UserCreate):
    user.password = get_password_hash(user.password)
    try:
        user_in_DB = crud.UserCrud.create(db, user)
    except:
        raise TOKEN_ERROR

    return user_in_DB


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("email")
        is_teacher = payload.get("is_teacher")
        if email is None:
            raise TOKEN_ERROR
        token_data = auth.TokenData(email=email, is_teacher=is_teacher)
    except JWTError:
        raise TOKEN_ERROR
    user = crud.UserCrud.get_by_email(db, token_data.email)

    if user is None:
        raise TOKEN_ERROR

    if not user.is_active:
        raise INACTIVE_USER_ERROR

    return user