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

def main():

    key = load_key()

    fernet = Fernet(key)

    while True:
        print("\n1. 회원가입  2. 로그인  3. 종료")
        choice = input("선택: ")

        if choice == "1":
            user_id = input("아이디 입력: ")
            if find_user(user_id):
                print("이미 존재하는 아이디입니다.")
                continue
            password = input("비밀번호 입력: ")
            encrypted_pw = fernet.encrypt(password.encode())
            save_user(user_id, encrypted_pw)
            print("회원가입 완료!")
