from repositories.external_server_repository import ExternalServerRepository

class ExternalAPIConfig:
    def __init__(self):
        external_servers = ExternalServerRepository().get_keys()
        self.NEWS_API_KEY = None
        self.THENEWSAPI_TOKEN = None
        for server in external_servers:
            if server["name"].lower() == "newsapi":
                self.NEWS_API_KEY = server.get("api_key")
            elif server["name"].lower() == "thenewsapi":
                self.THENEWSAPI_TOKEN = server.get("api_key")
