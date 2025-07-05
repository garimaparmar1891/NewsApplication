from utils.http_client import HttpClient
from utils.endpoints import GET_EXTERNAL_SERVERS, UPDATE_EXTERNAL_SERVER
from constants import messages as msg

class ExternalServerService:
    """Handles external server fetch and update operations."""

    @staticmethod
    def fetch_external_servers():
        """
        Fetches the list of external servers.
        Returns:
            tuple: (success: bool, data: list or str)
        """
        response = HttpClient.authorized_request("GET", GET_EXTERNAL_SERVERS)
        if response.ok:
            return True, response.json().get("data", [])
        return False, response.json().get("message", "Unknown error")

    @staticmethod
    def update_external_server_by_id(server_id, update_data):
        """
        Updates an external server by its ID.
        Args:
            server_id (str): The ID of the server to update.
            update_data (dict): The data to update.
        Returns:
            tuple: (success: bool, message: str)
        """
        endpoint = f"{UPDATE_EXTERNAL_SERVER}/{server_id}"
        response = HttpClient.authorized_request("PATCH", endpoint, json=update_data)

        if response.ok:
            return True, msg.EXTERNAL_SERVER_UPDATE_SUCCESS
        try:
            return False, msg.EXTERNAL_SERVER_UPDATE_FAILED.format(response.json().get("message", "Unknown error"))
        except Exception:
            return False, msg.EXTERNAL_SERVER_UPDATE_FAILED.format("Unexpected error")