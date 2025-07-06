from features.services.admin.external_server_service import ExternalServerService
from utils.response_handler import handle_response, handle_data_response
from utils.input_utils import get_valid_integer_input
from constants import messages as msg

class ExternalServerHandler:

    @staticmethod
    def view_all_external_servers():
        try:
            print(msg.EXTERNAL_SERVER_LIST_TITLE)
            response = ExternalServerService.fetch_external_servers()
            success, data = handle_data_response(response, msg.EXTERNAL_SERVER_FETCH_FAILED)
            
            if not success or not data:
                return False, msg.EXTERNAL_SERVER_NO_SERVERS_FOUND
                
            servers = data if isinstance(data, list) else []
            ExternalServerHandler._print_server_list(servers)
            return True, data
        except Exception as e:
            print(f"Error occurred while viewing external servers: {str(e)}")
            return False, f"Error: {str(e)}"

    @staticmethod
    def view_external_server_details():
        try:
            print(msg.EXTERNAL_SERVER_DETAILS_TITLE)
            response = ExternalServerService.fetch_external_servers()
            success, data = handle_data_response(response, msg.EXTERNAL_SERVER_FETCH_FAILED)
            
            if not success or not data:
                return False, msg.EXTERNAL_SERVER_NO_SERVERS_FOUND
                
            servers = data if isinstance(data, list) else []
            ExternalServerHandler._print_server_details(servers)
            return True, data
        except Exception as e:
            print(f"Error occurred while viewing external server details: {str(e)}")
            return False, f"Error: {str(e)}"

    @staticmethod
    def update_external_server():
        try:
            print(msg.EXTERNAL_SERVER_EDIT_TITLE)
            servers = ExternalServerHandler._fetch_servers()
            if not servers:
                return False, msg.EXTERNAL_SERVER_NO_SERVERS_FOUND
                
            server_id = ExternalServerHandler._get_server_id(servers)
            if not server_id:
                return False, "Invalid server ID"
                
            update_data = ExternalServerHandler._gather_update_input()
            
            if not update_data:
                return False, msg.EXTERNAL_SERVER_NO_UPDATE_FIELDS

            response = ExternalServerService.update_external_server(server_id, update_data)
            success, message = handle_response(
                response,
                msg.EXTERNAL_SERVER_UPDATE_SUCCESS,
                msg.EXTERNAL_SERVER_UPDATE_FAILED
            )
            
            print(message)
            return success, message
        except Exception as e:
            print(f"Error occurred while updating external server: {str(e)}")
            return False, f"Error: {str(e)}"

    @staticmethod
    def _fetch_servers():
        try:
            response = ExternalServerService.fetch_external_servers()
            success, data = handle_data_response(response, msg.EXTERNAL_SERVER_FETCH_FAILED)
            
            if not success or not data:
                return None
                
            return data if isinstance(data, list) else []
        except Exception as e:
            print(f"Error occurred while fetching servers: {str(e)}")
            return None

    @staticmethod
    def _get_server_id(servers):
        try:
            valid_ids = [server.get('id') for server in servers if server.get('id') is not None]
            server_id = get_valid_integer_input(msg.EXTERNAL_SERVER_ID_PROMPT, valid_ids)
            return server_id
        except Exception as e:
            print(f"Error occurred while getting server ID: {str(e)}")
            return None

    @staticmethod
    def _gather_update_input():
        try:
            update_data = {}
            
            name = input(msg.EXTERNAL_SERVER_NAME_PROMPT).strip()
            if name:
                update_data['name'] = name
                
            url = input(msg.EXTERNAL_SERVER_URL_PROMPT).strip()
            if url:
                update_data['url'] = url
                
            api_key = input(msg.EXTERNAL_SERVER_API_KEY_PROMPT).strip()
            if api_key:
                update_data['api_key'] = api_key
                
            isactive_input = input(msg.EXTERNAL_SERVER_ISACTIVE_PROMPT).strip()
            if isactive_input:
                try:
                    isactive_value = int(isactive_input)
                    if isactive_value in [0, 1]:
                        update_data['Is_Active'] = isactive_value
                    else:
                        print("Invalid value. Please enter 0 for inactive or 1 for active.")
                except ValueError:
                    print("Invalid input. Please enter a number (0 or 1).")
                
            return update_data if update_data else None
        except Exception as e:
            print(f"Error occurred while gathering update input: {str(e)}")
            return None

    @staticmethod
    def _print_server_list(servers):
        try:
            print(msg.EXTERNAL_SERVER_AVAILABLE_TITLE)
            for server in servers:
                print(f"  ID: {server.get('id', 'N/A')} | Name: {server.get('name', 'N/A')} | URL: {server.get('base_url', 'N/A')}")
     
        except Exception as e:
            print(f"Error occurred while printing server list: {str(e)}")

    @staticmethod
    def _print_server_details(servers):
        try:
            for server in servers:
                print(f"\nServer ID: {server.get('id', 'N/A')}")
                print(f"Name: {server.get('name', 'N/A')}")
                print(f"API Key: {server.get('api_key', 'N/A')}")
                print(f"Last Accessed: {server.get('last_accessed', 'N/A')}")
                print("\n")
        except Exception as e:
            print(f"Error occurred while printing server details: {str(e)}")
