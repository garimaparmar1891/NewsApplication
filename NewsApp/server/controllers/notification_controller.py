from flask import request
from flask_jwt_extended import get_jwt_identity
from http import HTTPStatus
from services.notification_service import NotificationService
from utils.response_utils import success_response, error_response
from constants import messages as msg


class NotificationController:
    def __init__(self):
        self.service = NotificationService()

    def get_unread_user_notifications(self):
        user_id = get_jwt_identity()
        data = self.service.get_unread_user_notifications(user_id)
        if not data:
            return self._error(msg.NO_NOTIFICATIONS, HTTPStatus.NOT_FOUND)
        return self._success(data=data)

    def get_user_preferences(self):
        user_id = get_jwt_identity()
        prefs = self.service.get_user_preferences(user_id)
        return self._success(data=prefs)

    def update_user_preferences(self):
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        preferences = data.get("categories", [])

        if not isinstance(preferences, list):
            return self._error(msg.INVALID_PREFERENCE_FORMAT)

        if self.service.update_user_preferences(user_id, preferences):
            return self._success(message=msg.PREFERENCES_UPDATED)

        return self._error(msg.PREFERENCES_UPDATE_FAILED)

    def send_email_notifications(self):
        user_id = get_jwt_identity()
        result = self.service.send_email_notifications(user_id)

        if result.get("success"):
            return self._success(message=result.get("message", msg.EMAIL_SENT_SUCCESS), data=result)

        return self._error(result.get("message", msg.EMAIL_SEND_FAILED))


    def _has_fields(self, data, fields):
        return data and all(data.get(field) for field in fields)

    def _success(self, data=None, message=None, status=HTTPStatus.OK):
        return success_response(data=data, message=message, status=status)

    def _error(self, message, status=HTTPStatus.BAD_REQUEST):
        return error_response(message=message, status=status)
