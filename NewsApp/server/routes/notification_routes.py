from flask import Blueprint
from flasgger import swag_from
from controllers.notification_controller import NotificationController
from utils.auth_decorators import user_required

notification_bp = Blueprint("notifications", __name__)
notification_controller = NotificationController()

@notification_bp.route("/api/notifications", methods=["GET"])
@user_required
@swag_from("../docs/notifications/get_notifications.yml")
def get_notifications():
    return notification_controller.get_notifications_for_user()

@notification_bp.route("/api/notifications/preferences", methods=["POST"])
@user_required
@swag_from("../docs/notifications/update_preferences.yml")
def update_preferences():
    return notification_controller.update_user_preferences()

@notification_bp.route("/api/notifications/preferences", methods=["GET"])
@user_required
@swag_from("../docs/notifications/get_preferences.yml")
def get_preferences():
    return notification_controller.get_user_preferences()

@notification_bp.route("/api/notifications/keywords", methods=["POST"])
@user_required
@swag_from("../docs/notifications/add_keyword.yml")
def add_keyword_to_category_route():
    return notification_controller.add_keyword_to_category()

@notification_bp.route("/api/notifications/send-email", methods=["POST"])
@user_required
@swag_from("../docs/notifications/send_email.yml")
def send_email_notifications():
    return notification_controller.send_email_notifications()
