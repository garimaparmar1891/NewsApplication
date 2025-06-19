from flask import request, jsonify
from http import HTTPStatus
from services.admin_service import AdminService
from utils.response_utils import success_response, error_response


class AdminController:
    def __init__(self):
        self.admin_service = AdminService()

    # ---------- External Servers ----------
    def get_external_servers(self):
        return success_response(data=self.admin_service.get_external_servers())

    def add_external_server(self):
        data = request.get_json()
        if not self._validate_required_fields(data, ["name", "base_url", "token"]):
            return self._missing_fields_response()

        if self.admin_service.add_external_server(data["name"], data["base_url"], data["token"]):
            return success_response(message="External server added", status=HTTPStatus.CREATED)
        return error_response("Failed to add external server", HTTPStatus.BAD_REQUEST)

    def update_external_server(self, server_id):
        data = request.get_json()
        result = self.admin_service.update_external_server(server_id, data)
        if result:
            return jsonify({"success": True, "message": "Server updated successfully"}), 200
        return jsonify({"success": False, "message": "Failed to update server"}), 400
    
    def delete_external_server(self, server_id):
        if self.admin_service.delete_external_server(server_id):
            return success_response(message="External server deleted")
        return error_response("External server not found", HTTPStatus.NOT_FOUND)

    # ---------- Categories ----------
    def get_categories(self):
        return success_response(data=self.admin_service.get_categories())

    def add_category(self):
        data = request.get_json()
        name = data.get("name") if data else None
        if not name:
            return error_response("Category name is required", HTTPStatus.BAD_REQUEST)

        if self.admin_service.add_category(name):
            return success_response(message="Category added", status=HTTPStatus.CREATED)
        return error_response("Failed to add category", HTTPStatus.BAD_REQUEST)

    def delete_category(self, category_id):
        if self.admin_service.delete_category(category_id):
            return success_response(message="Category deleted")
        return error_response("Category not found", HTTPStatus.NOT_FOUND)

    # ---------- Private Helpers ----------
    def _validate_required_fields(self, data, fields):
        return data and all(data.get(field) for field in fields)

    def _missing_fields_response(self):
        return error_response("Missing required fields", HTTPStatus.BAD_REQUEST)
