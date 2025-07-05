from flask import Blueprint
from flasgger import swag_from
from controllers.notification_controller import NotificationController
from utils.auth_decorators import user_required

notification_bp = Blueprint("notifications", __name__)
notification_controller = NotificationController()

@notification_bp.route("/api/notifications", methods=["GET"])
@user_required
@swag_from("../docs/notifications/get_notifications.yml")
def get_unread_user_notifications():
    return notification_controller.get_unread_user_notifications()

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

