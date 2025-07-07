import pytest
from services.notification_service import NotificationService, AdminNotifier
from utils.custom_exceptions import AppError
from http import HTTPStatus

class MockRepo:
    def get_unread_user_notifications(self, user_id):
        return ["notif1"] if user_id == 1 else []
    def mark_notifications_as_read(self, user_id):
        self.read_marked = True
    def get_user_preferences(self, user_id):
        return {"categories": [1, 2]}
    def update_user_preferences(self, user_id, preferences):
        self.updated = preferences
    def add_user_keyword(self, user_id, category_id, keyword):
        self.added = (user_id, category_id, keyword)

class MockAuthRepo:
    def get_admin_email(self):
        return "admin@example.com"

class MockEmailService:
    sent = False
    @staticmethod
    def send_email(to_email, subject, html_content):
        MockEmailService.sent = True

@pytest.fixture
def service():
    return NotificationService(repo=MockRepo(), auth_repo=MockAuthRepo())

@pytest.fixture
def admin_notifier(monkeypatch):
    monkeypatch.setattr("services.notification_service.EmailService", MockEmailService)
    return AdminNotifier(auth_repo=MockAuthRepo())


def test_get_unread_user_notifications_no_notifications(service):
    with pytest.raises(AppError) as exc:
        service.get_unread_user_notifications(2)
    assert exc.value.status_code == HTTPStatus.NOT_FOUND

def test_update_user_preferences_invalid_format(service):
    data = {"categories": "invalid"}
    with pytest.raises(AppError) as exc:
        service.update_user_preferences(1, data)
    assert exc.value.status_code == HTTPStatus.BAD_REQUEST

def test_add_keywords_from_preferences_adds_keyword(service):
    service.repo = MockRepo()
    service._add_keywords_from_preferences(1, [{"categoryId": 1, "keywords": ["k1"]}])
    assert service.repo.added == (1, 1, "k1")

def test_send_admin_email_sends_email(admin_notifier):
    admin_notifier.send_admin_email("subject", "body")
    assert MockEmailService.sent

def test_send_admin_email_no_admin(monkeypatch):
    class NoAdminRepo:
        def get_admin_email(self):
            return None
    notifier = AdminNotifier(auth_repo=NoAdminRepo())
    with pytest.raises(AppError) as exc:
        notifier.send_admin_email("subject", "body")
    assert exc.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
