from services.notification_service import NotificationService
from utils.exception_handler import handle_exceptions
from flask import request
from controllers.base_controller import BaseController


class NotificationController(BaseController):
    def __init__(self, service=None):
        super().__init__()
        self.service = service or NotificationService()

    @handle_exceptions()
    def get_unread_user_notifications(self):
        user_id = self._get_user_id()
        return self.service.get_unread_user_notifications(user_id)

    @handle_exceptions()
    def update_user_preferences(self):
        user_id = self._get_user_id()
        data = request.get_json() or {}
        return self.service.update_user_preferences(user_id, data)

    @handle_exceptions()
    def get_user_preferences(self):
        user_id = self._get_user_id()
        return self.service.get_user_preferences(user_id)

