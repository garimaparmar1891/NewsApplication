from repositories.admin_repository import AdminRepository
from constants import messages


class AdminService:
    def __init__(self):
        self.repository = AdminRepository()

    def get_external_servers(self):
        return self.repository.get_external_servers()

    def update_external_server(self, server_id, update_data):
        return self.repository.update_external_server(server_id, update_data)


    def get_categories(self):
        return self.repository.get_categories()

    def add_category(self, name):
        return self.repository.add_category(name)

    def hide_category(self, category_id):
        category = self.repository.get_category_by_id(category_id)
        if not category:
            raise ValueError(messages.CATEGORY_NOT_FOUND)
        
        self.repository.hide_category_by_id(category_id)
        return messages.CATEGORY_HIDDEN
