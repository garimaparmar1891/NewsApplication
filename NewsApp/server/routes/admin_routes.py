from flask import Blueprint
from controllers.admin_controller import AdminController
from flasgger import swag_from
from utils.auth_decorators import admin_required

admin_bp = Blueprint("admin", __name__)
admin_controller = AdminController()

@admin_bp.route("/api/admin/external-servers", methods=["GET"])
@admin_required
@swag_from("../docs/admin/get_external_servers.yml")
def get_external_servers():
    return admin_controller.get_external_servers()

@admin_bp.route("/api/admin/external-servers/<int:server_id>", methods=["PATCH"])
@admin_required
@swag_from("../docs/admin/update_external_server.yml")
def update_external_server(server_id):
    return admin_controller.update_external_server(server_id)

@admin_bp.route("/api/admin/categories", methods=["GET"])
@admin_required
@swag_from("../docs/admin/get_categories.yml")
def get_categories():
    return admin_controller.get_categories()

@admin_bp.route("/api/admin/categories", methods=["POST"])
@admin_required
@swag_from("../docs/admin/add_category.yml")
def add_category():
    return admin_controller.add_category()
