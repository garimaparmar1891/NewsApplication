from features.admin.external_server.external_server_service import ExternalServerService
from features.admin.utils.print_helpers import PrintHelpers
from features.admin.utils.input_helpers import InputHelpers
from constants import messages as msg

class ExternalServersManager:
    """Handles external server viewing and updating."""

    @staticmethod
    def view_all_external_servers():
        print("\n--- External Servers List ---")
        success, servers = ExternalServerService.fetch_external_servers()
        print(success, servers)
        if not success or not servers:
            print(msg.EXTERNAL_SERVER_NO_SERVERS_FOUND)
            return
        PrintHelpers.print_server_list(servers)

    @staticmethod
    def view_external_server_details():
        print("\n--- View External Server Details ---")
        success, servers = ExternalServerService.fetch_external_servers()
        if not success or not servers:
            print(msg.EXTERNAL_SERVER_NO_SERVERS_FOUND)
            return
        PrintHelpers.print_server_details(servers)

    @staticmethod
    def update_external_server():
        print("\n--- Edit External Server ---")
        server_id = ExternalServersManager._get_valid_server_id()
        if not server_id:
            return

        update_data = InputHelpers.gather_external_server_update_input()
        if not update_data:
            print(msg.EXTERNAL_SERVER_NO_UPDATE_FIELDS)
            return

        ExternalServerService.update_external_server_by_id(server_id, update_data)

    @staticmethod
    def _get_valid_server_id():
        server_id = input("Enter External Server ID to update: ").strip()
        if not server_id.isdigit():
            print(msg.EXTERNAL_SERVER_INVALID_ID)
            return None
        return int(server_id) 