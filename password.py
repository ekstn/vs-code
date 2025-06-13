# 터미널이나 cmd에 pip install cryptography 입력


import os
from cryptography.fernet import Fernet

user_db = "users.txt"

key = "secret.key"

def load_key():
    if os.path.exists(key):
        with open(key, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key, "wb") as f:
            f.write(key)
        return key