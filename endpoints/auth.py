# -*- coding: utf-8 -*-
'''The logic of authorization and receipt of the JWT token'''

from datetime import timedelta

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from core.config import ACCESS_TOKEN_EXPIRE_DAY
from custom_exceptions.exceptions import LOGIN_ERROR, REG_ERROR
from models import auth, users
from dependencies import security
from db.database import get_db
from sqlalchemy.orm import Session


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post("/registration/", response_model=auth.Token)
async def registration(user: users.UserCreate, db: Session = Depends(get_db)):
    db_user = security.get_user(db, user.email)
    if not db_user is None:
        raise REG_ERROR

    db_user = await security.save_user(db, user)
    if not db_user:
        raise LOGIN_ERROR

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_DAY)
    access_token = security.create_access_token(
        data={"email": user.email, "is_teacher": user.is_teacher}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@auth_router.post("/token/", response_model=auth.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise LOGIN_ERROR

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_DAY)
    access_token = security.create_access_token(
        data={"email": user.email, "is_teacher": user.is_teacher}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users/me/", response_model=users.UserOutside)
async def read_users_me(current_user: users.User = Depends(security.get_current_user)):
    return current_user

