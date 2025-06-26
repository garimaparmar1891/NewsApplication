from utils.http_client import authorized_request
from utils.endpoints import (
    GET_EXTERNAL_SERVERS,
    UPDATE_EXTERNAL_SERVER
)

SERVER_FIELDS = {
    "name": "Name",
    "base_url": "Base_Url",
    "api_key": "Api_key",
    "is_active": "Is_Active"
}

def print_server_list(servers):
    for idx, server in enumerate(servers, start=1):
        print(f"\n[{idx}] Server: {server.get('name')}")
        print(f"Active         : {'Yes' if server.get('is_active') else 'No'}")
        print(f"Last Accessed  : {server.get('last_Accessed')}")
        print("-" * 50)

def print_server_details(servers):
    print("\nServer Details")
    for idx, server in enumerate(servers, start=1):
        print(f"\n[{idx}] Server: {server.get('name')}")
        print(f"API Key       : {server.get('api_key')}")
        print("-" * 50)

def fetch_external_servers():
    response = authorized_request("GET", GET_EXTERNAL_SERVERS)
    if response.ok:
        return response.json().get("data", [])
    print("Failed to fetch servers:", response.json().get("message", "Unknown error"))
    return []

def view_all_external_servers():
    print("\n--- External Servers List ---")
    servers = fetch_external_servers()
    if not servers:
        print("No external servers found.")
        return
    print_server_list(servers)

def view_external_server_details():
    servers = fetch_external_servers()
    if not servers:
        print("No external servers found.")
        return
    print_server_details(servers)

def gather_update_data():
    name = input("New Name (leave blank to keep unchanged): ").strip()
    base_url = input("New Base URL (leave blank to keep unchanged): ").strip()
    api_key = input("New API Key (leave blank to keep unchanged): ").strip()
    is_active_input = input("Set Active? (yes/no/leave blank to keep unchanged): ").strip().lower()

    data = {}
    if name:
        data[SERVER_FIELDS["name"]] = name
    if base_url:
        data[SERVER_FIELDS["base_url"]] = base_url
    if api_key:
        data[SERVER_FIELDS["api_key"]] = api_key
    if is_active_input == "yes":
        data[SERVER_FIELDS["is_active"]] = True
    elif is_active_input == "no":
        data[SERVER_FIELDS["is_active"]] = False

    return data

def update_external_server():
    print("\n--- Edit External Server ---")
    server_id = input("Enter External Server ID to update: ").strip()
    if not server_id.isdigit():
        print("Invalid server ID.")
        return

    update_data = gather_update_data()
    if not update_data:
        print("No fields provided to update.")
        return

    endpoint = f"{UPDATE_EXTERNAL_SERVER}/{server_id}"
    response = authorized_request("PATCH", endpoint, json=update_data)
    if response.ok:
        print("External server updated successfully.")
    else:
        try:
            print("Failed to update server:", response.json().get("message", "Unknown error"))
        except Exception:
            print("Failed to update server: Unexpected error")