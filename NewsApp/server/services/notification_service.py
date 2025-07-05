from repositories.notification_repository import NotificationRepository
from repositories.auth_repository import AuthRepository
from utils.email_utils import EmailService
from constants import messages as msg
from http import HTTPStatus
from utils.custom_exceptions import AppError
from services.base_service import BaseService

class NotificationService(BaseService):
    def __init__(self, repo=None, auth_repo=None):
        super().__init__()
        self.repo = repo or NotificationRepository()
        self.auth_repo = auth_repo or AuthRepository()

    def get_unread_user_notifications(self, user_id):
        notifications = self.repo.get_unread_user_notifications(user_id)
        self.repo.mark_notifications_as_read(user_id)
        return self._handle_empty_result(notifications, msg.NO_NOTIFICATIONS, HTTPStatus.NOT_FOUND)

    def get_user_preferences(self, user_id):
        prefs = self.repo.get_user_preferences(user_id)
        return self._create_success_response(data=prefs)

    def update_user_preferences(self, user_id, data):
        preferences = data.get("categories", [])
        if not isinstance(preferences, list):
            raise AppError(msg.INVALID_PREFERENCE_FORMAT, HTTPStatus.BAD_REQUEST)
        
        self.repo.update_user_preferences(user_id, preferences)
        self._add_keywords_from_preferences(user_id, preferences)
        return self._create_success_response(message=msg.PREFERENCES_UPDATED)

    def _add_keywords_from_preferences(self, user_id, preferences):
        for pref in preferences:
            category_id = pref.get("categoryId")
            for keyword in pref.get("keywords", []):
                self.repo.add_user_keyword(user_id, category_id, keyword)

class AdminNotifier:
    def __init__(self, auth_repo=None):
        self.auth_repo = auth_repo or AuthRepository()

    def send_admin_email(self, subject, body):
        admin_email = self.auth_repo.get_admin_email()
        if not admin_email:
            raise AppError("No admin email found in database", HTTPStatus.INTERNAL_SERVER_ERROR)
        EmailService.send_email(to_email=admin_email, subject=subject, html_content=body)
