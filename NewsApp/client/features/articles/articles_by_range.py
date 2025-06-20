from utils.http_client import authorized_request
from utils.pagination import paginate_articles

def get_articles_by_range():
    print("\n--- Fetch Articles by Date Range ---")
    category = input("Optional Category (press Enter to skip): ")
    start = input("Start Date (YYYY-MM-DD): ")
    end = input("End Date (YYYY-MM-DD): ")

    params = {
        "start_date": start,
        "end_date": end
    }
    if category:
        params["category"] = category

    response = authorized_request("GET", "/api/articles/range", params=params)

    if response.ok:
        data = response.json()
        articles = data.get("data", [])
        if not articles:
            print("No articles found for the given range.")
        else:
            print(f"\nFound {len(articles)} article(s):\n")
            paginate_articles(articles)
    else:
        print("Error fetching articles:", response.text)
