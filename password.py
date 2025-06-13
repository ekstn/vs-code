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
    
def save_user(user_id, encrypted_pw):
    with open(user_db, "a") as f:
        f.write(f"{user_id} {encrypted_pw.decode()}\n")

def find_user(user_id):
    if not os.path.exists(user_db):
        return None
    with open(user_db, "r") as f:
        for line in f:
            stored_id, stored_pw = line.strip().split()
            if stored_id == user_id:
                return stored_pw.encode()
    return None