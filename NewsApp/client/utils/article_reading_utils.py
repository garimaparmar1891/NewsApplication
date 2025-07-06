from utils.http_client import HttpClient
from utils.endpoints import READ_HISTORY
from menu.menu_constants import ARTICLE_READING_TITLE
from menu.article_reading_menu import ArticleReadingMenu

class ArticleReader:

    @staticmethod
    def read_article(article):
        ArticleReader.print_article_details(article)
        article_id = article.get("Id")
        ArticleReader.record_read_history(article_id)

        while True:
            ArticleReadingMenu.display_menu()
            choice = ArticleReadingMenu.get_user_choice()
            
            should_continue = ArticleReadingMenu.handle_menu_choice(choice, article_id)
            if not should_continue:
                break

    @staticmethod
    def print_article_details(article):
        print(ARTICLE_READING_TITLE)
        print(f"Article ID : {article.get('Id')}")
        print(f"Title      : {article.get('Title')}")
        print(f"Content    : {article.get('Content', 'No content available.')}")
        print(f"Source     : {article.get('Source')}")
        print(f"Published  : {article.get('PublishedAt')}")
        print(f"URL        : {article.get('Url')}\n")

    @staticmethod
    def record_read_history(article_id):
        HttpClient.authorized_request("POST", READ_HISTORY.format(article_id=article_id))
