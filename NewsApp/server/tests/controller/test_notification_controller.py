import sys
import os
import pytest
from unittest.mock import Mock, patch
from controllers.notification_controller import NotificationController



class TestNotificationController:
    def setup_method(self):
        self.mock_service = Mock()
        self.controller = NotificationController(service=self.mock_service)

    @patch('controllers.notification_controller.BaseController._get_user_id')
    def test_get_unread_user_notifications_returns_service_response(self, mock_get_user_id):
        mock_get_user_id.return_value = 1
        expected_response = {"notifications": []}
        self.mock_service.get_unread_user_notifications.return_value = expected_response

        result = self.controller.get_unread_user_notifications()

        assert result == expected_response
        self.mock_service.get_unread_user_notifications.assert_called_once_with(1)

    @patch('controllers.notification_controller.BaseController._get_user_id')
    def test_get_user_preferences_returns_service_response(self, mock_get_user_id):
        mock_get_user_id.return_value = 1
        expected_response = {"preferences": {"email": True}}
        self.mock_service.get_user_preferences.return_value = expected_response

        result = self.controller.get_user_preferences()

        assert result == expected_response
        self.mock_service.get_user_preferences.assert_called_once_with(1)
