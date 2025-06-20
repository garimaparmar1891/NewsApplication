from repositories.notification_repository import NotificationRepository
from repositories.user_repository import UserRepository
from utils.email_utils import EmailService


class NotificationService:
    def __init__(self):
        self.repo = NotificationRepository()
        self.user_repo = UserRepository()

    # ---------- Public Methods ----------

    def get_notifications_since_last_login(self, user_id):
        return self.repo.get_notifications_since_last_login(user_id)

    def update_user_preferences_and_keywords(self, user_id, preferences):
        try:
            self.repo.update_user_preferences(user_id, preferences)
            self._add_keywords_from_preferences(user_id, preferences)
            return True
        except Exception as e:
            print(f"Failed to update preferences: {e}")
            return False

    def send_email_notifications(self, user_id):
        user = self._get_user(user_id)
        if not user:
            return {"success": False, "message": "User not found"}

        keyword_map = self._get_user_keywords(user_id)
        if not keyword_map:
            return {"success": False, "message": "No keywords found"}

        matched_articles = self._get_matched_articles(user_id, keyword_map)
        if not matched_articles:
            return {"success": False, "message": "No matching articles"}
        # print("-------------------------", matched_articles)
        if self._send_email_digest(user, matched_articles):
            self._mark_articles_sent(user_id, matched_articles)
            return {"success": True, "message": f"Sent {len(matched_articles)} article(s)"}

        return {"success": False, "message": "Failed to send email"}

    def get_user_preferences(self, user_id):
        return self.repo.get_user_preferences(user_id)

    def get_user_notifications(self, user_id):
        notifications = self.repo.get_unread_notifications(user_id)
        self.repo.mark_notifications_as_read(user_id)
        return notifications

    def get_user_keywords_by_category(self, user_id):
        return self.repo.get_user_keywords(user_id)

    def add_user_keyword(self, user_id, category_id, keyword):
        if self.repo.add_user_keyword(user_id, category_id, keyword):
            return {"success": True, "message": "Keyword added successfully"}
        return {"success": False, "message": "Keyword already exists or failed to add"}

    # ---------- Private Helpers ----------

    def _add_keywords_from_preferences(self, user_id, preferences):
        for pref in preferences:
            category_id = pref.get("categoryId")
            print('category to add keyword',category_id)
            if pref.get("keywords"):
                for keyword in pref["keywords"]:
                    self.repo.add_user_keyword(user_id, category_id, keyword)

    
    def _get_user(self, user_id):
        return self.user_repo.get_user_by_id(user_id)

    def _get_user_keywords(self, user_id):
        keyword_map = {}
        for item in self.repo.get_user_keywords(user_id):
            category_id = item["categoryId"]
            keyword = item["keyword"].lower()
            keyword_map.setdefault(category_id, []).append(keyword)
        return keyword_map

    def _get_matched_articles(self, user_id, keyword_map):
        matched = []
        articles = self.repo.get_unsent_articles_by_keywords(user_id, keyword_map)

        for article in articles:
            category_id = article.get("CategoryId")
            title = article.get("Title", "")
            content = article.get("Content", "")
            text = f"{title} {content}".lower()

            for keyword in keyword_map.get(category_id, []):
                if keyword in text:
                    matched.append(article)
                    break
        return matched

    def _send_email_digest(self, user, articles):
        subject = "Your Keyword-Based News Digest"
        email = user["email"]
        name = user["username"]
        body = self._build_email_body(name, articles)
        return EmailService.send_email(email, subject, body)

    def _build_email_body(self, name, articles):
        body = f"Hi {name},<br><br>Here are your matched articles:<br><ul>"

        for article in articles:
            body += f"""
                <li style="margin-bottom: 20px; list-style-type: none; border: 1px solid #ddd; padding: 15px; border-radius: 5px;">
                    <p><strong>Article ID:</strong> {article.get('Id')}</p>
                    <p><strong>Title:</strong> {article.get('Title')}</p>
                    <p><strong>Content:</strong> {article.get('Content', '')}</p>
                    <p><strong>Source:</strong> {article.get('Source')}</p>
                    <p><strong>Category ID:</strong> {article.get('CategoryId')}</p>
                    <p><strong>Published At:</strong> {article.get('PublishedAt')}</p>
                    <p><strong>Fetched At:</strong> {article.get('FetchedAt')}</p>
                    <p><strong>URL:</strong> <a href="{article.get('Url')}" target="_blank">{article.get('Url')}</a></p>
                </li>
            """


        body += "</ul><br>Regards,<br>News Aggregator Team"
        return body


    def _mark_articles_sent(self, user_id, articles):
        article_ids = [a["Id"] for a in articles]
        self.repo.mark_articles_as_sent(user_id, article_ids)
