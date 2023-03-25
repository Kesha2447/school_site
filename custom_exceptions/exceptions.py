# -*- coding: utf-8 -*-
'''Module for storing exceptions'''

import fastapi

TOKEN_ERROR = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="Invalid user data",
    headers={"WWW-Authenticate": "Bearer"},
)

LOGIN_ERROR = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

INACTIVE_USER_ERROR = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_400_BAD_REQUEST,
    detail="Inactive user"
)

REG_ERROR = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_400_BAD_REQUEST,
    detail="This email is already in use"
)

SUBJECT_NOT_FOUNT_ERROR = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_400_BAD_REQUEST,
    detail="The item with this id was not found"
)

SUBJECT_NOT_UNIQUE_ERROR = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_400_BAD_REQUEST,
    detail="The name is not unique"
)