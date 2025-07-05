from utils.http_client import HttpClient
from utils.endpoints import TODAY_HEADLINES

class TodayHeadlinesService:
    @staticmethod
    def fetch_today_headlines():
        return HttpClient.authorized_request("GET", TODAY_HEADLINES) 