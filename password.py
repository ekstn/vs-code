# 터미널이나 cmd에 pip install cryptography 입력


import os
from cryptography.fernet import Fernet
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

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

def register():
    user_id = id_entry.get().strip()
    pw = pw_entry.get().strip()
    pw_confirm = confirm_entry.get().strip()

    if find_user(user_id):
        messagebox.showerror("오류", "이미 존재하는 아이디입니다.")
        return
    if pw != pw_confirm:
        messagebox.showerror("오류", "비밀번호가 일치하지 않습니다.")
        return
    if len(pw) < 4:
        messagebox.showerror("오류", "비밀번호는 4자 이상이어야 합니다.")
        return

    encrypted_pw = fernet.encrypt(pw.encode())
    save_user(user_id, encrypted_pw)
    write_log("회원가입", user_id)
    messagebox.showinfo("성공", "회원가입 완료!")

def login():
    user_id = id_entry.get().strip()
    pw = pw_entry.get().strip()
    stored_pw_enc = find_user(user_id)

    if not stored_pw_enc:
        messagebox.showerror("오류", "등록되지 않은 아이디입니다.")
        return

    try:
        decrypted_pw = fernet.decrypt(stored_pw_enc).decode()
        if pw == decrypted_pw:
            write_log("로그인", user_id)
            messagebox.showinfo("성공", "로그인 성공!")
        else:
            messagebox.showerror("오류", "비밀번호가 틀렸습니다.")
    except:
        messagebox.showerror("오류", "복호화 오류 발생")

def change_password():
    user_id = id_entry.get().strip()
    current_pw = pw_entry.get().strip()
    new_pw = confirm_entry.get().strip()

    stored_pw_enc = find_user(user_id)
    if not stored_pw_enc:
        messagebox.showerror("오류", "사용자 정보 없음.")
        return

    try:
        decrypted_pw = fernet.decrypt(stored_pw_enc).decode()
        if decrypted_pw != current_pw:
            messagebox.showerror("오류", "현재 비밀번호가 일치하지 않습니다.")
            return
    except:
        messagebox.showerror("오류", "복호화 오류")
        return

    if new_pw == current_pw:
        messagebox.showerror("오류", "새 비밀번호는 현재 비밀번호와 달라야 합니다.")
        return
    if len(new_pw) < 4:
        messagebox.showerror("오류", "비밀번호는 4자 이상이어야 합니다.")
        return

    encrypted_pw = fernet.encrypt(new_pw.encode())
    delete_user(user_id)
    save_user(user_id, encrypted_pw)
    write_log("비밀번호 변경", user_id)
    messagebox.showinfo("성공", "비밀번호 변경 완료")

def delete_account():
    user_id = id_entry.get().strip()
    pw = pw_entry.get().strip()
    stored_pw_enc = find_user(user_id)

    if not stored_pw_enc:
        messagebox.showerror("오류", "등록되지 않은 아이디입니다.")
        return
    try:
        decrypted_pw = fernet.decrypt(stored_pw_enc).decode()
        if pw == decrypted_pw:
            delete_user(user_id)
            write_log("탈퇴", user_id)
            messagebox.showinfo("성공", "사용자 탈퇴 완료")
        else:
            messagebox.showerror("오류", "비밀번호가 틀렸습니다.")
    except:
        messagebox.showerror("오류", "복호화 오류")


key = load_key()
fernet = Fernet(key)

root = tk.Tk()
root.title("암호화 회원관리 시스템")
root.geometry("400x300")

tk.Label(root, text="아이디:").pack()
id_entry = tk.Entry(root)
id_entry.pack()

tk.Label(root, text="비밀번호:").pack()
pw_entry = tk.Entry(root, show="*")
pw_entry.pack()

tk.Label(root, text="비밀번호 확인 or 변경할 비밀번호:").pack()
confirm_entry = tk.Entry(root, show="*")
confirm_entry.pack()

btn_frame1 = tk.Frame(root)
btn_frame1.pack(pady=5)
tk.Button(btn_frame1, text="회원가입", width=15, command=register).pack(side="left", padx=5)
tk.Button(btn_frame1, text="로그인", width=15, command=login).pack(side="left", padx=5)

btn_frame2 = tk.Frame(root)
btn_frame2.pack(pady=5)
tk.Button(btn_frame2, text="비밀번호 변경", width=15, command=change_password).pack(side="left", padx=5)
tk.Button(btn_frame2, text="회원 탈퇴", width=15, command=delete_account).pack(side="left", padx=5)

tk.Button(root, text="종료", bg="red", fg="white", width=7, command=root.quit).pack(pady=10)

root.mainloop()
