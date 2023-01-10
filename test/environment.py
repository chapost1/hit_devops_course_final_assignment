import os
from enum import Enum


APP_URL = os.environ.get('APP_URL', 'http://127.0.0.1:5500/app/index.html')


class AuthCredentials(str, Enum):
    username = os.environ.get('USERNAME', 'admin')
    password = os.environ.get('PASSWORD', 'admin')
