# -*- coding: utf-8 -*-
'''Prescribe paths for the site pages'''

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from dependencies import security
from models import users


static_router = APIRouter()


@static_router.get('/')
async def get_wrapper():
    with open('static/wrapper.html', encoding='utf-8') as f:
        result_html = f.read()
            
    return HTMLResponse(result_html)


@static_router.get('/site/index')
async def get_auth(current_user: users.User = Depends(security.get_current_user)):
    with open('static/index.html', encoding='utf-8') as f:
        result_html = f.read()
        
        result_html.format(user_name=current_user.full_name)
    return HTMLResponse(result_html)


@static_router.get('/site/auth')
async def get_auth():
    with open('static/auth.html', encoding='utf-8') as f:
        result_html = f.read()
            
    return HTMLResponse(result_html)


@static_router.get('/site/lesson')
async def get_auth():
    with open('static/lesson.html', encoding='utf-8') as f:
        result_html = f.read()
            
    return HTMLResponse(result_html)