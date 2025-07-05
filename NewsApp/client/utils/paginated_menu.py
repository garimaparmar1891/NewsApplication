from utils.header import HeaderUtils
from utils.token_storage import TokenStorage
from utils.http_client import HttpClient
from utils.read_article import ArticleReader
from utils.endpoints import (
    SAVE_ARTICLE,
    REPORT_ARTICLE
)

ITEMS_PER_PAGE = 5

class PaginatedMenu:
    """Handles interactive paginated menu for articles."""

    def __init__(self, articles, context_label="Articles"):
        self.articles = articles
        self.context_label = context_label
        self.page = 0
        self.total_pages = (len(articles) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    def show(self):
        while True:
            HeaderUtils.print_welcome_message()
            start_index, end_index = self.print_articles_page()
            print(f"Page {self.page + 1} of {self.total_pages}")
            print("\nOptions:")
            print("1. Read article by ID")
            print("2. Save article by ID")
            print("3. Next page")
            print("4. Previous page")
            print("5. Go back to main menu")
            print("6. Logout")
            print("7. Report article by ID")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                article_id_input = self.prompt_article_id("read")
                self._handle_read_article(article_id_input)
            elif choice == "2":
                article_id_input = self.prompt_article_id("save")
                self._handle_save_article(article_id_input)
            elif choice == "3":
                if end_index >= len(self.articles):
                    print("You are on the last page.")
                else:
                    self.page += 1
            elif choice == "4":
                if self.page == 0:
                    print("You are already on the first page.")
                else:
                    self.page -= 1
            elif choice == "5":
                break
            elif choice == "6":
                TokenStorage.clear_token()
                print("Logged out successfully.")
                exit()
            elif choice == "7":
                article_id_input = self.prompt_article_id("report")
                self._handle_report_article(article_id_input)
            else:
                print("Invalid choice. Please try again.")

    def print_articles_page(self):
        start_index = self.page * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE
        current_articles = self.articles[start_index:end_index]
        print(f"\n{self.context_label}:\n")
        for article in current_articles:
            print(f"(Article ID: {article.get('Id')}) → {article.get('Title')}\n")
        return start_index, end_index

    @staticmethod
    def prompt_article_id(action):
        return input(f"Enter article ID to {action}: ").strip()

    def _handle_read_article(self, article_id_input):
        if article_id_input.isdigit():
            article_id = int(article_id_input)
            article = next((a for a in self.articles if a["Id"] == article_id), None)
            if article:
                ArticleReader.read_article(article)
            else:
                print("Article ID not found.")
        else:
            print("Invalid input. Please enter a valid numeric article ID.")

    def _handle_save_article(self, article_id_input):
        if article_id_input.isdigit():
            article_id = int(article_id_input)
            article = next((a for a in self.articles if a["Id"] == article_id), None)
            if article:
                self.save_article(article_id)
            else:
                print("Article ID not found.")
        else:
            print("Invalid input. Please enter a valid numeric article ID.")

    def _handle_report_article(self, article_id_input):
        if article_id_input.isdigit():
            article_id = int(article_id_input)
            article = next((a for a in self.articles if a["Id"] == article_id), None)
            if article:
                self.report_article(article_id)
            else:
                print("Article ID not found.")
        else:
            print("Invalid input. Please enter a valid numeric article ID.")

    @staticmethod
    def save_article(article_id):
        save_resp = HttpClient.authorized_request("POST", SAVE_ARTICLE.format(article_id=article_id))
        if save_resp.ok:
            print("Article saved successfully.")
        else:
            print("Failed to save article:", save_resp.json().get("message", save_resp.text))

    @staticmethod
    def report_article(article_id):
        reason = input("Enter reason for reporting this article: ").strip()
        if not reason:
            print("Report reason cannot be empty.")
            return
        report_resp = HttpClient.authorized_request("POST", REPORT_ARTICLE.format(article_id=article_id), json={"reason": reason})
        if report_resp.ok:
            print("Report submitted successfully.")
        else:
            print("Failed to report article:", report_resp.json().get("message", report_resp.text))