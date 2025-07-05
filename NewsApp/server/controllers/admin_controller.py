from services.admin_service import AdminService
from utils.exception_handler import handle_exceptions
from typing import cast
from controllers.base_controller import BaseController

class AdminController(BaseController):
    def __init__(self):
        super().__init__()
        self.admin_service = AdminService()

    @handle_exceptions()
    def get_external_servers(self):
        return self.admin_service.get_external_servers()

    @handle_exceptions()
    def update_external_server(self, server_id):
        data, error = self._validate_json_data()
        if error:
            return error
        return self.admin_service.update_external_server(server_id, data)

    @handle_exceptions()
    def get_categories(self):
        return self.admin_service.get_categories()

    @handle_exceptions()
    def add_category(self):
        data, error = self._validate_json_data(required_fields=["name"])
        if error:
            return error
        data = cast(dict, data)
        return self.admin_service.add_category(data["name"])
