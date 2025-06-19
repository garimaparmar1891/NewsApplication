from datetime import datetime
from utils.token_storage import get_user_info

def print_welcome_message():
    user_info = get_user_info()
    
    username = user_info.get("username", "User")

    now = datetime.now()
    date_str = now.strftime("%d-%b-%Y")
    time_str = now.strftime("%I:%M%p")

    print(f"\nWelcome to the News Application, {username}! Date: {date_str}")
    print(f"Time: {time_str}")
    print("Please choose the options below\n")
