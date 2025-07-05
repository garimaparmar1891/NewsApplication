from datetime import datetime
from utils.token_storage import TokenStorage

class HeaderUtils:
    """Utility class for printing headers and user info."""

    @staticmethod
    def print_welcome_message():
        username = HeaderUtils.get_username()
        date_str, time_str = HeaderUtils.get_current_datetime()
        print(f"\nWelcome to the News Application, {username}! Date: {date_str}")
        print(f"Time: {time_str}")
        print("Please choose the options below\n")

    @staticmethod
    def get_username():
        user_info = TokenStorage.get_user_info()
        return user_info.get("username", "User")

    @staticmethod
    def get_current_datetime():
        now = datetime.now()
        date_str = now.strftime("%d-%b-%Y")
        time_str = now.strftime("%I:%M%p")
        return date_str, time_str