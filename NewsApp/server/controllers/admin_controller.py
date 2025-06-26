from flask import request
from http import HTTPStatus
from services.admin_service import AdminService
from utils.response_utils import success_response, error_response
from constants import messages


class AdminController:
    def __init__(self):
        self.admin_service = AdminService()

    def get_external_servers(self):
        servers = self.admin_service.get_external_servers()
        return success_response(data=servers)

    def update_external_server(self, server_id):
        data = request.get_json()
        success = self.admin_service.update_external_server(server_id, data)
        return self._build_response({
            "success": success,
            "success_msg": messages.EXTERNAL_SERVER_UPDATED,
            "error_msg": messages.EXTERNAL_SERVER_UPDATE_FAILED
        })


    def get_categories(self):
        categories = self.admin_service.get_categories()
        return success_response(data=categories)

    def add_category(self):
        data = request.get_json()
        name = data.get("name") if data else None
        if not name:
            return self._missing_fields_response(messages.CATEGORY_NAME_REQUIRED)

        success = self.admin_service.add_category(name)
        return self._build_response({
            "success": success,
            "success_msg": messages.CATEGORY_ADDED,
            "error_msg": messages.CATEGORY_ADD_FAILED,
            "status": HTTPStatus.CREATED
        })

    def hide_category(self, category_id):
        try:
            message = self.admin_service.hide_category(category_id)
            return success_response(message=message)
        except ValueError as ve:
            return error_response(str(ve), HTTPStatus.NOT_FOUND)
        except Exception:
            return error_response(messages.CATEGORY_HIDE_FAILED, HTTPStatus.INTERNAL_SERVER_ERROR)


    def _missing_fields_response(self, message=messages.MISSING_REQUIRED_FIELDS):
        return error_response(message, HTTPStatus.BAD_REQUEST)

    def _build_response(self, info: dict):
        if info.get("success"):
            return success_response(
                message=info.get("success_msg"),
                status=info.get("status", HTTPStatus.OK)
            )
        return error_response(
            info.get("error_msg"),
            HTTPStatus.BAD_REQUEST if info.get("status", HTTPStatus.OK) == HTTPStatus.OK else info.get("status")
        )
