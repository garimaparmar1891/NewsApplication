from flask import request
from http import HTTPStatus
from services.admin_service import AdminService
from utils.response_utils import success_response, error_response


class AdminController:
    def __init__(self):
        self.admin_service = AdminService()

    def get_external_servers(self):
        servers = self.admin_service.get_external_servers()
        return success_response(data=servers)

    def add_external_server(self):
        data = request.get_json()
        if not self._has_fields(data, ["name", "base_url", "token"]):
            return self._missing_fields_response()

        success = self.admin_service.add_external_server(
            data["name"], data["base_url"], data["token"]
        )
        return self._response(success, "External server added", "Failed to add external server", HTTPStatus.CREATED)

    def update_external_server(self, server_id):
        data = request.get_json()
        success = self.admin_service.update_external_server(server_id, data)
        return self._response(success, "Server updated successfully", "Failed to update server")

    def delete_external_server(self, server_id):
        success = self.admin_service.delete_external_server(server_id)
        return self._response(success, "External server deleted", "External server not found", HTTPStatus.NOT_FOUND)

    def get_categories(self):
        categories = self.admin_service.get_categories()
        return success_response(data=categories)

    def add_category(self):
        data = request.get_json()
        name = data.get("name") if data else None
        if not name:
            return self._missing_fields_response("Category name is required")

        success = self.admin_service.add_category(name)
        return self._response(success, "Category added", "Failed to add category", HTTPStatus.CREATED)

    def delete_category(self, category_id):
        success = self.admin_service.delete_category(category_id)
        return self._response(success, "Category deleted", "Category not found", HTTPStatus.NOT_FOUND)

    def _has_fields(self, data, fields):
        return data and all(data.get(field) for field in fields)

    def _missing_fields_response(self, message="Missing required fields"):
        return error_response(message, HTTPStatus.BAD_REQUEST)

    def _response(self, success, success_msg, error_msg, status=HTTPStatus.OK):
        if success:
            return success_response(message=success_msg, status=status)
        return error_response(error_msg, HTTPStatus.BAD_REQUEST if status == HTTPStatus.OK else status)
