# -*- coding: utf-8 -*-
'''Models for performing authentication'''

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
    is_teacher: bool