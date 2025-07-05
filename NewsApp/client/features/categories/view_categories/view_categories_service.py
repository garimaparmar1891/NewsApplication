from tkinter import YES


class CategoryService:
    @staticmethod
    def fetch_categories():
        from utils.http_client import HttpClient
        from utils.endpoints import GET_CATEGORIES
        try:
            response = HttpClient.authorized_request("GET", GET_CATEGORIES)
            if response.status_code != 200:
                print("Failed to fetch categories.")
                return []
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            print("Error fetching categories:", str(e))
            return []