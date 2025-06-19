from repositories.admin_repository import AdminRepository
from typing import List, Dict

class AdminService:
    def __init__(self):
        self.repo = AdminRepository()

    def get_external_servers(self) -> List[Dict]:
        return self.repo.get_external_servers()

    def add_external_server(self, name: str, base_url: str, api_key: str) -> bool:
        return self.repo.add_external_server(name, base_url, api_key)

    def delete_external_server(self, server_id: int) -> bool:
        return self.repo.delete_external_server(server_id)

    def get_categories(self) -> List[Dict]:
        return self.repo.get_categories()

    def add_category(self, name: str) -> bool:
        return self.repo.add_category(name)

    def delete_category(self, category_id: int) -> bool:
        return self.repo.delete_category(category_id)

    def update_external_server(self, server_id, data):
        return self.repo.update_external_server(server_id, data)