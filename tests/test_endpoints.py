# -*- coding: utf-8 -*-
'''Testing data parsing via rest api'''

import os
import sys
import time
import unittest
from fastapi.testclient import TestClient
os.chdir('..')
sys.path.append(".")
from main import app


if __name__ == '__main__':
    unittest.main()