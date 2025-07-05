from features.articles.today_headlines.today_headlines_service import TodayHeadlinesService
from utils.paginated_menu import PaginatedMenu

class TodayHeadlinesManager:
    @staticmethod
    def show_today_headlines():
        print("\n--- Today's Headlines ---")
        response = TodayHeadlinesService.fetch_today_headlines()
        if not response.ok:
            print(response.json().get("message", response.text))
            return
        articles = response.json().get("data", [])
        if not articles:
            print("No headlines available today.")
            return
        PaginatedMenu(articles, context_label="Today's Articles").show() 