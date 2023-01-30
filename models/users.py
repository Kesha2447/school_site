# -*- coding: utf-8 -*-
'''Declaring pedantic models for processing user information'''

from typing import Union
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserEntry(UserBase):
    password: str = Field(min_length=6)


class UserInfo(UserBase):
    full_name: str = Field(regex='^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$')
    is_teacher: bool = Field(default=False)


class UserCreate(UserEntry, UserInfo):
    pass


class UserData(BaseModel):
    id: int
    is_active: bool
    last_auth: datetime = Field(default=datetime.now())
    photo: Union[str, None] = Field(default=None)


class User(UserCreate, UserData):
    class Config:
        orm_mode = True


class UserOutside(UserInfo, UserData):
    class Config:
        orm_mode = True
