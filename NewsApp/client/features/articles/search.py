from utils.http_client import authorized_request
from utils.token_storage import save_token
from utils.pagination import paginate_articles

def search_articles():
    q = input("Enter keyword: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    while True:
        params = {"q": q, "start_date": start_date, "end_date": end_date}
        res = authorized_request("GET", "/api/articles/search", params=params)
        if res.status_code != 200:
            print("Failed to fetch articles.")
            return

        data = res.json()
        articles = data.get("data", [])

        if not articles:
            print("No more articles found.")
            return
        paginate_articles(articles)
        break

