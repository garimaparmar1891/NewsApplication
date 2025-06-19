import json
import os

TOKEN_FILE = "token.txt"
USER_FILE = "user_info.json"

def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None

def save_user_info(user_info):
    with open(USER_FILE, "w") as f:
        json.dump(user_info, f)

def get_user_info():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def clear_token():
    global _token
    _token = None
