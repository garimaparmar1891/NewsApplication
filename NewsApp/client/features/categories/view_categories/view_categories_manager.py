from .view_categories_service import CategoryService

class CategoryManager:
    @staticmethod
    def display_categories():
        categories = CategoryService.fetch_categories()
        CategoryManager.print_categories(categories)

    @staticmethod
    def print_categories(categories):
        if not categories:
            print("No categories found.")
            return
        print("\nAvailable Categories:")
        print("1. All News")  # First option for all articles
        option_map = {1: "all"}
        for idx, cat in enumerate(categories, start=2):
            print(f"{idx}. {cat['name']}")
            option_map[idx] = cat['id']
        return option_map 