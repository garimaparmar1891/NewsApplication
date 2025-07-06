import json
import os

class TokenStorage:

    TOKEN_FILE = "token.txt"
    USER_FILE = "user_info.json"

    @classmethod
    def save_token(cls, token):
        with open(cls.TOKEN_FILE, "w") as f:
            f.write(token or "")

    @classmethod
    def get_token(cls):
        if os.path.exists(cls.TOKEN_FILE):
            with open(cls.TOKEN_FILE, "r") as f:
                return f.read().strip() or None
        return None

    @classmethod
    def save_user_info(cls, user_info):
        with open(cls.USER_FILE, "w") as f:
            json.dump(user_info, f)

    @classmethod
    def get_user_info(cls):
        if os.path.exists(cls.USER_FILE):
            with open(cls.USER_FILE, "r") as f:
                return json.load(f)
        return {}

    @classmethod
    def clear_token(cls):
        if os.path.exists(cls.TOKEN_FILE):
            os.remove(cls.TOKEN_FILE)
