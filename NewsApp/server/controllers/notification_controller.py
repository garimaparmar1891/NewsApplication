from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from http import HTTPStatus
from services.notification_service import NotificationService
from utils.response_utils import success_response, error_response


class NotificationController:
    def __init__(self):
        self.service = NotificationService()

    def get_notifications_for_user(self):
        user_id = get_jwt_identity()
        data = self.service.get_user_notifications(user_id)
        return self._success(data=data)

    def get_notifications_since_last_login(self):
        user_id = get_jwt_identity()
        data = self.service.get_notifications_since_last_login(user_id)

        if not data:
            return self._error("No notifications found", HTTPStatus.NOT_FOUND)
        return self._success(data=data)

    def update_user_preferences(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        preferences = data.get("categories", [])
        print(preferences)
        if not isinstance(preferences, list):
            return self._error("Invalid input format. 'categories' must be a list.")

        if self.service.update_user_preferences_and_keywords(user_id, preferences):
            return self._success(message="Preferences and keywords updated successfully")
        return self._error("Failed to update preferences")

    def send_email_notifications(self):
        user_id = get_jwt_identity()
        result = self.service.send_email_notifications(user_id)

        if result.get("success"):
            return self._success(message=result.get("message"), data=result)
        return self._error(result.get("message", "Failed to send email"))

    def add_keyword_to_category(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        if not self._has_fields(data, ["category_id", "keyword"]):
            return self._error("Category ID and keyword are required")

        result = self.service.add_user_keyword(user_id, data["category_id"], data["keyword"])
        if result.get("success"):
            return self._success(message="Keyword added successfully", data=result)
        return self._error(result.get("message", "Failed to add keyword"))

    def get_user_preferences(self):
        user_id = get_jwt_identity()
        prefs = self.service.get_user_preferences(user_id)
        return self._success(data=prefs)

    def _has_fields(self, data, fields):
        return data and all(data.get(field) for field in fields)

    def _success(self, data=None, message=None, status=HTTPStatus.OK):
        return success_response(data=data, message=message, status=status)

    def _error(self, message, status=HTTPStatus.BAD_REQUEST):
        return error_response(message=message, status=status)
