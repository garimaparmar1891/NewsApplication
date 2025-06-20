from utils.http_client import authorized_request
from utils.pagination import paginate_articles
def get_today_headlines():
    print("\n--- Today's Headlines ---")
    response = authorized_request("GET", "/api/articles/today")

    if not response.ok:
        print("Failed to fetch today's headlines:", response.json().get("message", response.text))
        return

    articles = response.json().get("data", [])
    
    if not articles:
        print("No headlines available today.")
        return
    else:
        paginate_articles(articles)


    while True:
        choice = input("\nEnter article number to save or 'q' to go back: ").strip()
        if choice.lower() == "q":
            break
        if choice.isdigit() and 1 <= int(choice) <= len(articles):
            article_id = articles[int(choice) - 1]["Id"]
            response = authorized_request("POST", f"/api/articles/{article_id}/save")
            if response.ok:
                print("Article saved.")
            else:
                print("Error saving article:", response.json().get("message", response.text))
        else:
            print("Invalid choice. Try again.")
