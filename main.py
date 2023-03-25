# -*- coding: utf-8 -*-
'''A module for processing requests for information about twitter users using FastAPI'''

import fastapi
import uvicorn
from fastapi.staticfiles import StaticFiles
from endpoints import auth, lessons, static

app = fastapi.FastAPI()
app.include_router(auth.auth_router)
app.include_router(lessons.subject_router)
app.include_router(lessons.lesson_router)
app.include_router(lessons.result_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(static.static_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=9000, reload=True)