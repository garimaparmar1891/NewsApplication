from repositories.admin_repository import AdminRepository
from constants import messages
from utils.custom_exceptions import AppError
from http import HTTPStatus
from services.base_service import BaseService

class AdminService(BaseService):
    def __init__(self):
        super().__init__()
        self.repository = AdminRepository()

    def get_external_servers(self):
        servers = self.repository.get_external_servers()
        return self._create_success_response(data=servers)

    def update_external_server(self, server_id, update_data):
        success = self.repository.update_external_server(server_id, update_data)
        if not success:
            raise AppError(messages.EXTERNAL_SERVER_UPDATE_FAILED, HTTPStatus.BAD_REQUEST)
        return self._create_success_response(message=messages.EXTERNAL_SERVER_UPDATED)

    def get_categories(self):
        categories = self.repository.get_categories()
        return self._create_success_response(data=categories)

    def add_category(self, name):
        success = self.repository.add_category(name)
        if not success:
            raise AppError(messages.CATEGORY_ADD_FAILED, HTTPStatus.INTERNAL_SERVER_ERROR)
        return self._create_success_response(message=messages.CATEGORY_ADDED)
