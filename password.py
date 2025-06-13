# 터미널이나 cmd에 pip install cryptography 입력


import os
from cryptography.fernet import Fernet
from datetime import datetime

user_db = "users.txt"

key_file = "secret.key"

log_file = "log.txt"


def load_key():
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()
    else:
        new_key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(new_key)
        return new_key
    

def write_log(action, user_id):
    with open(log_file, "a") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {action} - {user_id}\n")


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


def delete_user(user_id):
    if not os.path.exists(user_db):
        return
    with open(user_db, "r") as f:
        lines = f.readlines()
    with open(user_db, "w") as f:
        for line in lines:
            if not line.startswith(user_id + " "):
                f.write(line)


def main():

    key = load_key()

    fernet = Fernet(key)

    while True:
        print("\n1. 회원가입  2. 로그인  3.사용자 탈퇴  4. 종료")
        choice = input("선택: ")

        if choice == "1":
            user_id = input("아이디 입력: ")
            if find_user(user_id):
                print("이미 존재하는 아이디입니다.")
                continue
            password = input("비밀번호 입력: ")
            encrypted_pw = fernet.encrypt(password.encode())
            save_user(user_id, encrypted_pw)
            write_log("회원가입", user_id)
            print("회원가입 완료!")

        elif choice == "2":
            user_id = input("아이디 입력: ")
            stored_pw_enc = find_user(user_id)
            if not stored_pw_enc:
                print("등록되지 않은 아이디입니다.")
                continue
            password = input("비밀번호 입력: ")
            try:
                decrypted_pw = fernet.decrypt(stored_pw_enc).decode()
                if password == decrypted_pw:
                    write_log("로그인", user_id)
                    print("로그인 성공!")
                else:
                    print("비밀번호가 틀렸습니다.")
            except:
                print("복호화 오류 발생")

        elif choice == "3":
            user_id = input("아이디 입력: ").strip()
            pw = input("비밀번호 입력: ").strip()
            stored_pw_enc = find_user(user_id)
            if not stored_pw_enc:
                print("등록되지 않은 아이디입니다.")
                continue
            try:
                decrypted_pw = fernet.decrypt(stored_pw_enc).decode()
                if pw == decrypted_pw:
                    delete_user(user_id)
                    write_log("탈퇴", user_id)
                    print("사용자 탈퇴 완료.")
                else:
                    print("비밀번호가 틀렸습니다.")
            except:
                print("복호화 오류 발생")


        elif choice == "4":
            print("프로그램 종료")
            break
        else:
            print("올바른 선택이 아닙니다.")


if __name__ == "__main__":
    main()