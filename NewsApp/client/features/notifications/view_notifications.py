from utils.paginate_notifications import paginate_notifications

def view_notifications():
    from utils.http_client import authorized_request
    response = authorized_request("GET", "/api/notifications")
    
    if response.ok:
        notifications = response.json().get("data", [])
        paginate_notifications(notifications)
    else:
        print("Failed to fetch notifications.")
