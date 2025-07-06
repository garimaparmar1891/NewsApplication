from repositories.article_visibility_repository import ArticleVisibilityRepository
from repositories.article_repository import ArticleRepository
from repositories.auth_repository import AuthRepository
from services.notification_service import AdminNotifier
from constants import messages
from utils.custom_exceptions import AppError
from http import HTTPStatus
from services.base_service import BaseService


class ArticleVisibilityService(BaseService):
    def __init__(self):
        super().__init__()
        self.repo = ArticleVisibilityRepository()
        self.article_repo = ArticleRepository()
        self.auth_repo = AuthRepository()
        self.admin_notifier = AdminNotifier(self.auth_repo)

    def report_article(self, article_id, user_id, reason):
        self._validate_required_fields(article_id, user_id, reason, 
                                     error_message=messages.REPORT_FIELDS_REQUIRED)
        try:
            self.repo.add_report(article_id, user_id, reason)
            self._process_article_report(article_id, user_id, reason)
            return self._create_success_response(message=messages.ARTICLE_REPORTED_SUCCESS)
        except ValueError as e:
            if "already reported" in str(e).lower():
                raise AppError(str(e), HTTPStatus.CONFLICT)
            raise

    def get_all_reported_articles(self):
        articles = self.repo.get_all_reported_articles()
        return self._create_success_response(data=articles)

    def hide_article(self, article_id):
        self._validate_article_exists(article_id)
        self.repo.hide_article(article_id)
        return self._create_success_response(message=messages.ARTICLE_HIDDEN_SUCCESS)

    def unhide_article(self, article_id):
        self._validate_article_exists(article_id)
        self.repo.unhide_article(article_id)
        self.repo.clear_article_reports(article_id)
        return self._create_success_response(message=messages.ARTICLE_UNHIDDEN_SUCCESS)

    def toggle_article_visibility(self, article_id, action):
        if action == "hide":
            return self.hide_article(article_id)
        elif action == "unhide":
            return self.unhide_article(article_id)
        else:
            raise AppError(messages.INVALID_VISIBILITY_ACTION, HTTPStatus.BAD_REQUEST)

    def hide_category(self, category_id):
        self.repo.hide_category(category_id)
        return self._create_success_response(message=messages.CATEGORY_HIDDEN_SUCCESS)

    def unhide_category(self, category_id):
        self.repo.unhide_category(category_id)
        return self._create_success_response(message=messages.CATEGORY_UNHIDDEN_SUCCESS)

    def toggle_category_visibility(self, category_id, action):
        if action == "hide":
            return self.hide_category(category_id)
        elif action == "unhide":
            return self.unhide_category(category_id)
        else:
            raise AppError(messages.INVALID_VISIBILITY_ACTION, HTTPStatus.BAD_REQUEST)

    def add_blocked_keyword(self, keyword):
        self._validate_required_fields(keyword, error_message=messages.KEYWORD_REQUIRED)
        self.repo.add_blocked_keyword(keyword)
        return self._create_success_response(message=messages.BLOCKED_KEYWORD_ADDED)

    def get_blocked_keywords(self):
        keywords = self.repo.get_blocked_keywords()
        return self._create_success_response(data=keywords)

    def delete_blocked_keyword(self, keyword_id):
        affected_rows = self.repo.delete_blocked_keyword(keyword_id)
        if affected_rows == 0:
            raise AppError(messages.KEYWORD_NOT_FOUND, HTTPStatus.NOT_FOUND)
        self.repo.unhide_articles_after_keyword_removal()
        return self._create_success_response(message=messages.BLOCKED_KEYWORD_DELETED)

    def is_article_blocked(self, content):
        blocked = self.repo.is_keyword_blocked(content)
        return self._create_success_response(data={"blocked": blocked})

    def _process_article_report(self, article_id, user_id, reason):
        article = self.article_repo.get_article_by_id(article_id)
        user = self.auth_repo.get_user_by_id(user_id)
        
        if not article or not user:
            raise AppError(messages.ARTICLE_OR_USER_NOT_FOUND, HTTPStatus.NOT_FOUND)

        if self._should_hide_article(article_id):
            self.repo.hide_article(article_id)

        self._notify_admin_of_report(article, user, user_id, article_id, reason)

    def _validate_article_exists(self, article_id):
        if not self.repo.article_exists(article_id):
            raise AppError(messages.ARTICLE_NOT_FOUND, HTTPStatus.NOT_FOUND)

    def _should_hide_article(self, article_id):
        count = self.repo.get_report_count(article_id)
        return count >= messages.REPORT_THRESHOLD

    def _notify_admin_of_report(self, article, user, user_id, article_id, reason):
        article_title = article.get('Title', 'Unknown Title') if isinstance(article, dict) else 'Unknown Title'
        subject = f"Article Reported: {article_title}"
        body = self._build_report_notification_body(user, user_id, article, article_id, reason)
        self.admin_notifier.send_admin_email(subject, body)

    def _build_report_notification_body(self, user, user_id, article, article_id, reason):
        user_email = user[2] if user and len(user) > 2 else 'Unknown'
        article_title = article.get('Title', 'Unknown Title') if isinstance(article, dict) else 'Unknown Title'
        
        return (
            f"User '{user_email}' (ID: {user_id}) has reported article "
            f"'{article_title}' (ID: {article_id}).\n"
            f"Reason: {reason}"
        )
