# -*- coding: utf-8 -*-

import os
from starlette.config import Config

path = os.path.dirname(__file__)
config = Config(path + '/.env')

try:
    DATABASE_URL = config.get('DATABASE_URL')
    SECRET_KEY = config.get('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_DAY = float(config.get('ACCESS_TOKEN_EXPIRE_DAY'))
except:
    print('The .env file was not filled in!!!')