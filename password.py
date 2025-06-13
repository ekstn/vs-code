# 터미널이나 cmd에 pip install cryptography 입력


import os
from cryptography.fernet import Fernet

user_db = "users.txt"

key = "secret.key"