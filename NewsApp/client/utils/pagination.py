from features.articles.save_unsave import save_article
from utils.token_storage import clear_token
from utils.header import print_welcome_message
from utils.http_client import authorized_request

def paginate_articles(articles, items_per_page=5):
    total = len(articles)
    if total == 0:
        print("No articles to display.")
        return

    page = 0
    while True:
        print_welcome_message()
        start = page * items_per_page
        end = start + items_per_page
        current_page_articles = articles[start:end]

        for article in current_page_articles:
            print(f"\nArticle Id: {article.get('Id')}")
            print(f"{article.get('Title', '')}\n")
            
            content = article.get('Content') or ''
            print(f"{content[:300]}…")

            print(f"\nSource: {article.get('Source', '')}")
            print(f"URL: {article.get('Url', 'N/A')}")
            print(f"Category: {article.get('Category', '')}")
            print(f"Published At: {article.get('PublishedAt', '')}")
            print("-" * 60)


        print(f"\nShowing {start + 1}-{min(end, total)} of {total} articles\n")
        print("1. Go to Next Page")
        print("2. Go to Previous Page")
        print("3. Save Article by ID")
        print("4. Like/Dislike Article by ID")
        print("5. Go Back to Main Menu")
        print("6. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            if end >= total:
                print("You are on the last page.")
            else:
                page += 1

        elif choice == "2":
            if page == 0:
                print("You are already on the first page.")
            else:
                page -= 1

        elif choice == "3":
            save_article()
            break

        elif choice == "4":
            article_id = input("Enter Article ID: ").strip()
            reaction = input("Enter 'like' or 'dislike': ").strip().lower()
            if reaction not in ["like", "dislike"]:
                print("Invalid reaction. Must be 'like' or 'dislike'.")
                continue
            response = authorized_request("POST", f"/api/reactions/{article_id}/{reaction}")
            if response.ok:
                print(f"Article {reaction}d successfully.")
            else:
                print("Failed to react:", response.json().get("message", response.text))


        elif choice == "5":
            break

        elif choice == "6":
            clear_token()
            print("Logged out successfully.")
            exit()

        else:
            print("Invalid choice. Please try again.")
