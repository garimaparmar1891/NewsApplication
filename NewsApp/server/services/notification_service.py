
from repositories.notification_repository import NotificationRepository
from repositories.user_repository import UserRepository
from repositories.auth_repository import AuthRepository
from utils.email_utils import EmailService
from constants import messages as msg


class NotificationService:
    def __init__(self):
        self.repo = NotificationRepository()
        self.auth_repo = AuthRepository()

    def get_unread_user_notifications(self, user_id):
        notifications = self.repo.get_unread_user_notifications(user_id)
        self.repo.mark_notifications_as_read(user_id)
        return notifications

    def update_user_preferences(self, user_id, preferences):
        try:
            self.repo.update_user_preferences(user_id, preferences)
            self._add_keywords_from_preferences(user_id, preferences)
            return True
        except Exception as e:
            print(f"[Update Preferences Error]: {e}")
            return False

    def get_user_preferences(self, user_id):
        return self.repo.get_user_preferences(user_id)

    def send_email_notifications(self, user_id):
        user = self._get_user(user_id)
        if not user:
            print("User not found")
            return {"success": False, "message": "User not found"}

        keyword_map = self._get_user_keywords(user_id)

        if keyword_map:
            matched_articles = self._get_matched_articles(user_id, keyword_map)
            if not matched_articles:
                print("No matching articles")
                return {"success": False, "message": "No matching articles"}
        else:
            print("No keywords found — using enabled categories")
            enabled_category_ids = self.repo.get_enabled_category_ids(user_id)
            if not enabled_category_ids:
                return {"success": False, "message": "No enabled categories"}

            matched_articles = self.repo.get_articles_by_categories(user_id, enabled_category_ids)
            if not matched_articles:
                return {"success": False, "message": "No articles found in enabled categories"}

        print(f"Sending email with {len(matched_articles)} articles")

        if self._send_email_digest(user, matched_articles):
            self._mark_articles_sent(user_id, matched_articles)
            return {"success": True, "message": f"Sent {len(matched_articles)} article(s)"}

        return {"success": False, "message": "Failed to send email"}


    def _get_user(self, user_id):
        return self.auth_repo.get_user_by_id(user_id)

    def _get_user_keywords(self, user_id):
        keyword_map = {}
        for item in self.repo.get_user_keywords(user_id):
            category_id = item["categoryId"]
            keyword = item["keyword"].lower()
            keyword_map.setdefault(category_id, []).append(keyword)
        return keyword_map

    def _get_matched_articles(self, user_id, keyword_map):
        articles = self.repo.get_unsent_articles_by_keywords(user_id, keyword_map)
        matched = []

        for article in articles:
            text = f"{article.get('Title', '')} {article.get('Content', '')}".lower()
            category_keywords = keyword_map.get(article.get("CategoryId"), [])

            if any(keyword in text for keyword in category_keywords):
                matched.append(article)

        return matched

    def _send_email_digest(self, user, articles):
        subject = "Your Keyword-Based News Digest"
        email_body = self._build_email_body(user["username"], articles)
        return EmailService.send_email(user["email"], subject, email_body)

    def _build_email_body(self, name, articles):
        body = f"Hi {name},<br><br>Here are your matched articles:<br><ul>"
        for article in articles:
            body += f"""
                <li style="margin-bottom: 20px; list-style-type: none; border: 1px solid #ddd; padding: 15px; border-radius: 5px;">
                    <p><strong>Article ID:</strong> {article.get('Id')}</p>
                    <p><strong>Title:</strong> {article.get('Title')}</p>
                    <p><strong>Content:</strong> {article.get('Content', '')}</p>
                    <p><strong>Source:</strong> {article.get('Source')}</p>
                    <p><strong>Published At:</strong> {article.get('PublishedAt')}</p>
                    <p><strong>URL:</strong> <a href="{article.get('Url')}" target="_blank">{article.get('Url')}</a></p>
                </li>
            """
        body += "</ul><br>Regards,<br>News Aggregator Team"
        return body

    def _add_keywords_from_preferences(self, user_id, preferences):
        for pref in preferences:
            category_id = pref.get("categoryId")
            for keyword in pref.get("keywords", []):
                self.repo.add_user_keyword(user_id, category_id, keyword)


    def _mark_articles_sent(self, user_id, articles):
        article_ids = [a["Id"] for a in articles]
        self.repo.mark_articles_as_sent(user_id, article_ids)

        for article in articles:
            message = f"New article: {article.get('Title')}"
            self.repo.insert_notification(user_id, article["Id"], message)
