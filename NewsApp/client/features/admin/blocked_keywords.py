from utils.http_client import authorized_request
from utils.endpoints import ADD_BLOCKED_KEYWORD, GET_BLOCKED_KEYWORDS

def add_blocked_keyword():
    keyword = input("Enter keyword to block: ").strip()
    if not keyword:
        print("Keyword cannot be empty.")
        return
    response = authorized_request("POST", ADD_BLOCKED_KEYWORD, json={"keyword": keyword})
    if response.ok:
        print("Keyword blocked.")
    else:
        print("Failed to block keyword.")

def view_blocked_keywords():
    response = authorized_request("GET", GET_BLOCKED_KEYWORDS)
    if response.ok:
        keywords = response.json().get("data", [])
        if not keywords:
            print("No blocked keywords found.")
        else:
            print("\nBlocked Keywords:")
            for kw in keywords:
                print(f" - {kw}")
    else:
        print("Failed to fetch blocked keywords.")