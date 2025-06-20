from repositories.admin_repository import AdminRepository


class AdminService:
    def __init__(self):
        self.repo = AdminRepository()

    def get_external_servers(self):
        return self.repo.get_external_servers()

    def add_external_server(self, name, base_url, api_key):
        return self.repo.add_external_server(name, base_url, api_key)

    def update_external_server(self, server_id, data):
        return self.repo.update_external_server(server_id, data)

    def delete_external_server(self, server_id):
        return self.repo.delete_external_server(server_id)

    def get_categories(self):
        return self.repo.get_categories()

    def add_category(self, name):
        return self.repo.add_category(name)

    def delete_category(self, category_id):
        return self.repo.delete_category(category_id)
