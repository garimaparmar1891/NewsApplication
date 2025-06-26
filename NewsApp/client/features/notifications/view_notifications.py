from utils.paginated_menu import interactive_paginated_menu
from utils.http_client import authorized_request
from utils.endpoints import GET_NOTIFICATIONS

def view_notifications():
    response = fetch_notifications()
    print_notifications_status(response)

def fetch_notifications():
    return authorized_request("GET", GET_NOTIFICATIONS)

def print_notifications_status(response):
    if response.ok:
        notifications = response.json().get("data", [])
        interactive_paginated_menu(notifications)
    else:
        print("Failed to fetch notifications.")
