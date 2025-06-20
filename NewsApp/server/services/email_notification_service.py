from repositories.notification_repository import NotificationRepository
from repositories.article_repository import ArticleRepository
from repositories.login_history_repository import LoginHistoryRepository
from repositories.user_keyword_repository import UserKeywordRepository
from utils.email_utils import EmailService
from datetime import datetime


class EmailNotificationService:
    def __init__(self):
        self.notification_repo = NotificationRepository()
        self.article_repo = ArticleRepository()
        self.login_repo = LoginHistoryRepository()
        self.keyword_repo = UserKeywordRepository()

    def send_notifications(self):
        print("Email notification job started.")
        
        users = self.notification_repo.get_users_with_enabled_preferences()
        
        for user in users:
            user_id = user["user_id"]
            email = user["email"]
            username = user.get("username", "User")

            category_ids = self.notification_repo.get_enabled_category_ids(user_id)
            if not category_ids:
                print("No enabled categories found. Skipping user.")
                continue

            last_login = self.login_repo.get_last_login(user_id) or datetime(2000, 1, 1)

            articles = self.article_repo.get_articles_for_categories_since(category_ids, last_login)
            if not articles:
                print("No articles found. Skipping user.")
                continue

            keyword_map = self.keyword_repo.get_user_keywords_map(user_id)

            matched_articles = self._filter_articles_by_keywords(articles, keyword_map)
            if not matched_articles:
                continue

            self._store_notifications(user_id, matched_articles)
            print("Stored notifications in database.")

            self._send_email_notification(email, username, matched_articles)
            print(f"Email sent to {email}")

    # ---------- Private Helpers ----------

    def _filter_articles_by_keywords(self, articles, keyword_map):
        matched = []
        print("🔍 Sample article:", articles[0], type(articles[0]))

        for article in articles:
            category_id = article.get("Id")
            title = article.get("Title", "") or ""
            content = article.get("Content", "") or ""
            category_id = article.get("CategoryId")

            text = f"{title} {content}".lower()
            keywords = keyword_map.get(category_id, [])

            if any(keyword.lower() in text for keyword in keywords):
                matched.append(article)

        return matched


    def _store_notifications(self, user_id, articles):
        for article in articles:
            message = f"New article matched your keyword: {article['Title']}"
            self.notification_repo.insert_notification(user_id, article["Id"], message)


    def _send_email_notification(self, recipient, username, articles):
        subject = f"News updates for {username}"
        body = self._compose_email_body(username, articles)
        try:
            EmailService.send_email(recipient, subject, body)

        except Exception as e:
            print(f"Failed to send email to {recipient}: {e}")


    def _compose_email_body(self, username, articles):
        body = f"<p>Hi {username},</p>"
        body += "<p>Here are the latest articles in your subscribed categories:</p>"

        for article in articles:
            body += (
                f"<hr>"
                f"<b>Article ID:</b> {article.get('Id')}<br>"
                f"<b>Title:</b> {article.get('Title')}<br>"
                f"<b>Content:</b> {article.get('Content', '')}<br>"
                f"<b>Source:</b> {article.get('Source')}<br>"
                f"<b>Published:</b> {article.get('PublishedAt')}<br>"
                f"<b>URL:</b> <a href='{article.get('Url')}'>{article.get('Url')}</a><br>"
                f"------------------------------\n\n"
            )

        body += "<br><p>Regards,<br>News Aggregator Team</p>"
        return body
