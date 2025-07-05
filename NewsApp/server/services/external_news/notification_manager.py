from utils.email_utils import EmailService
from constants.messages import SENT_EMAIL_NOTIFICATIONS, ERROR_FETCHING_FROM_SOURCE, ERROR_IN_SEND_NOTIFICATIONS
from typing import List, Dict, Optional

class ArticleFormatter:
    @staticmethod
    def format_article_row(row) -> Dict:
        try:
            return {
                "Id": row[0],
                "Title": row[1],
                "Content": row[2],
                "Source": row[3],
                "Url": row[4],
                "CategoryId": row[5],
                "PublishedAt": row[6]
            }
        except Exception:
            return {}

class EmailBuilder:
    @staticmethod
    def build_digest_email(username: str, articles: List[Dict]) -> str:
        try:
            body = f"Hi {username},<br><br>Here are your matched articles:<br><ul>"
            for article in articles:
                body += EmailBuilder._build_article_html(article)
            body += "</ul><br>Regards,<br>News Aggregator Team"
            return body
        except Exception:
            return ""
    
    @staticmethod
    def _build_article_html(article: Dict) -> str:
        try:
            return f"""
                <li style="margin-bottom: 20px; list-style-type: none; border: 1px solid #ddd; padding: 15px; border-radius: 5px;">
                    <p><strong>Title:</strong> {article.get('Title')}</p>
                    <p><strong>Content:</strong> {article.get('Content', '')}</p>
                    <p><strong>Source:</strong> {article.get('Source')}</p>
                    <p><strong>Published At:</strong> {article.get('PublishedAt')}</p>
                    <p><strong>URL:</strong> <a href="{article.get('Url')}" target="_blank">{article.get('Url')}</a></p>
                </li>
            """
        except Exception:
            return ""

class ArticleMatcher:
    def __init__(self, notification_repo):
        self.notification_repo = notification_repo
    
    def get_matched_articles_for_user(self, user_id: int) -> List[Dict]:
        try:
            keyword_articles = self._get_articles_by_keywords(user_id)
            if keyword_articles:
                return keyword_articles
            
            return self._get_articles_by_categories(user_id)
        except Exception:
            return []
    
    def _get_articles_by_keywords(self, user_id: int) -> List[Dict]:
        try:
            keyword_map = self._get_user_keywords(user_id)
            if not keyword_map:
                return []
            
            articles = self._aggregate_articles_by_keywords(user_id, keyword_map)
            return self._filter_articles_by_keywords(articles, keyword_map)
        except Exception:
            return []
    
    def _get_articles_by_categories(self, user_id: int) -> List[Dict]:
        try:
            enabled_category_ids = self.notification_repo.get_enabled_category_ids(user_id)
            if not enabled_category_ids:
                return []
            
            matched_articles = self.notification_repo.get_articles_by_categories(user_id, enabled_category_ids)
            return [ArticleFormatter.format_article_row(row) for row in matched_articles]
        except Exception:
            return []
    
    def _get_user_keywords(self, user_id: int) -> Dict:
        keyword_map = {}
        try:
            for item in self.notification_repo.get_user_keywords(user_id):
                category_id = item["categoryId"]
                keyword = item["keyword"].lower()
                keyword_map.setdefault(category_id, []).append(keyword)
        except Exception:
            pass
        return keyword_map
    
    def _aggregate_articles_by_keywords(self, user_id: int, keyword_map: Dict) -> List[Dict]:
        results = []
        try:
            for category_id, keywords in keyword_map.items():
                for keyword in keywords:
                    rows = self.notification_repo.get_unsent_articles(user_id, category_id, keyword)
                    results.extend([ArticleFormatter.format_article_row(row) for row in rows])
        except Exception:
            pass
        return results
    
    def _filter_articles_by_keywords(self, articles: List[Dict], keyword_map: Dict) -> List[Dict]:
        matched = []
        try:
            for article in articles:
                text = f"{article.get('Title', '')} {article.get('Content', '')}".lower()
                category_keywords = keyword_map.get(article.get("CategoryId"), [])
                if any(keyword in text for keyword in category_keywords):
                    matched.append(article)
        except Exception:
            pass
        return matched

class NotificationProcessor:
    def __init__(self, notification_repo, notification_service):
        self.notification_repo = notification_repo
        self.notification_service = notification_service
        self.article_matcher = ArticleMatcher(notification_repo)
    
    def process_user_notifications(self, user_id: int) -> int:
        try:
            user = self._get_user_data(user_id)
            if not user:
                return 0
            
            matched_articles = self.article_matcher.get_matched_articles_for_user(user_id)
            if not matched_articles:
                return 0
            
            if self._send_email_digest(user, matched_articles):
                self._mark_articles_sent(user["id"], matched_articles)
                self._create_notifications_for_sent_articles(user["id"], matched_articles)
                return len(matched_articles)
            
            return 0
        except Exception as e:
            print(ERROR_IN_SEND_NOTIFICATIONS.format(error=e))
            return 0
    
    def _get_user_data(self, user_id: int) -> Optional[Dict]:
        try:
            user_row = self.notification_service.auth_repo.get_user_by_id(user_id)
            if not user_row:
                return None
            
            return {
                "id": user_row[0],
                "username": user_row[1],
                "email": user_row[2]
            }
        except Exception:
            return None
    
    def _send_email_digest(self, user: Dict, articles: List[Dict]) -> bool:
        try:
            subject = "Your Keyword-Based News Digest"
            email_body = EmailBuilder.build_digest_email(user["username"], articles)
            return EmailService.send_email(user["email"], subject, email_body)
        except Exception:
            return False
    
    def _mark_articles_sent(self, user_id: int, articles: List[Dict]) -> None:
        try:
            article_ids = [article["Id"] for article in articles]
            self.notification_repo.mark_articles_as_sent(user_id, article_ids)
        except Exception:
            pass
    
    def _create_notifications_for_sent_articles(self, user_id: int, articles: List[Dict]) -> None:
        try:
            for article in articles:
                message = f"New article: {article.get('Title')}"
                self.notification_repo.insert_notification(user_id, article["Id"], message)
        except Exception:
            pass

class NotificationManager:
    def __init__(self, notification_repo, notification_service):
        self.notification_repo = notification_repo
        self.notification_service = notification_service
        self.notification_processor = NotificationProcessor(notification_repo, notification_service)
    
    def check_and_notify_users(self, articles, user_notification_count):
        if not articles:
            return
        
        users_with_prefs = self.notification_repo.get_users_with_enabled_preferences()
        
        for user in users_with_prefs:
            user_id = user.get("user_id")
            if not user_id:
                continue
            
            try:
                count = self.notification_processor.process_user_notifications(user_id)
                if count > 0:
                    user_notification_count[user["email"]] = count
                    print(SENT_EMAIL_NOTIFICATIONS.format(count=count, email=user.get('email')))
            except Exception as e:
                print(ERROR_FETCHING_FROM_SOURCE.format(name=user.get('email'), error=e))
