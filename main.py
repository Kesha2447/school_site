# -*- coding: utf-8 -*-
'''A module for processing requests for information about twitter users using FastAPI'''

import fastapi
import uvicorn


app = fastapi.FastAPI()

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000)