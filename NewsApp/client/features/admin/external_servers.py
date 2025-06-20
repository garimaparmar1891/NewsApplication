from utils.http_client import authorized_request

def view_all_external_servers():
    print("\n--- External Servers List ---")
    response = authorized_request("GET", "/api/admin/external-servers")
    print(response)
    if response.ok:
        servers = response.json().get("data", [])
        print(servers)
        if not servers:
            print("No external servers found.")
        else:
            for idx, server in enumerate(servers, start=1):
                print(f"\n[{idx}] Server: {server.get('name')}")
                print(f"Active         : {'Yes' if server.get('is_active') else 'No'}")
                print(f"Last Accessed  : {server.get('last_Accessed')}")
                print("-" * 50)
    else:
        print("Failed to fetch servers:", response.json().get("message", "Unknown error"))

def view_external_server_details():
    response = authorized_request("GET", f"/api/admin/external-servers")
    if response.ok:
        server = response.json().get("data", {})
        for idx, server in enumerate(server, start=1):
            print(f"\nServer Details ")
            print(f"\n[{idx}] Server: {server.get('name')}")
            print(f"API Key        : {server.get('api_key')}")
    else:
        print("Failed to fetch server details:", response.json().get("message", "Unknown error"))

def update_external_server():
    print("\nEdit External Server")
    server_id = input("Enter External Server ID to update: ").strip()

    if not server_id.isdigit():
        print("Invalid server ID.")
        return

    name = input("New Name (leave blank to keep unchanged): ").strip()
    base_url = input("New Base URL (leave blank to keep unchanged): ").strip()
    api_key = input("New API Key (leave blank to keep unchanged): ").strip()
    is_active_input = input("Set Active? (yes/no/leave blank to keep unchanged): ").strip().lower()

    update_data = {}

    if name:
        update_data["Name"] = name
    if base_url:
        update_data["Base_Url"] = base_url
    if api_key:
        update_data["Api_key"] = api_key
    if is_active_input == "yes":
        update_data["Is_Active"] = True
    elif is_active_input == "no":
        update_data["Is_Active"] = False

    if not update_data:
        print("No fields provided to update.")
        return

    response = authorized_request(
        method="PATCH",
        endpoint=f"/api/admin/external-servers/{server_id}",
        json=update_data
    )
    print(response)
    if response.ok:
        print("External server updated successfully.")
    else:
        try:
            print("Failed to update server:", response.json().get("message", "Unknown error"))
        except:
            print("Failed to update server: Unexpected error.")