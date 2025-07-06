from utils.http_client import HttpClient
from utils.endpoints import GET_EXTERNAL_SERVERS, UPDATE_EXTERNAL_SERVER

class ExternalServerService:

    @staticmethod
    def fetch_external_servers():
        return HttpClient.authorized_request("GET", GET_EXTERNAL_SERVERS)

    @staticmethod
    def update_external_server(server_id, update_data):
        endpoint = f"{UPDATE_EXTERNAL_SERVER}/{server_id}"
        return HttpClient.authorized_request("PATCH", endpoint, json=update_data)
