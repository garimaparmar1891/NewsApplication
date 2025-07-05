from utils.http_client import HttpClient
from utils.endpoints import (
    ADD_CATEGORY,
    HIDE_UNHIDE_ARTICLE,
    HIDE_UNHIDE_CATEGORY,
    GET_CATEGORY_FOR_ADMIN,
)
from features.admin.utils.print_helpers import PrintHelpers
from features.admin.categories.categories_service import CategoryService


class CategoryManager:
    """Handles category and visibility management."""

    @staticmethod
    def add_news_category():
        category_name = input("Enter new category name: ").strip()
        if not category_name:
            print("Category name cannot be empty.")
            return

        response = CategoryService.add_category(category_name)
        if response.ok:
            print(f"Category '{category_name}' added successfully.")
        else:
            error_msg = response.json().get("message", "Unknown error")
            print(f"Failed to add category: {error_msg}")

    @staticmethod
    def hide_unhide_article():
        CategoryManager._hide_unhide_entity("article")

    @staticmethod
    def hide_unhide_category():
        CategoryManager._hide_unhide_entity("category")

    @staticmethod
    def _hide_unhide_entity(entity_type):
        # Show categories before prompt (only for category)
        valid_ids = []
        if entity_type == "category":
            valid_ids = CategoryManager._display_available_categories()

        entity_id = input(f"Enter {entity_type.capitalize()} ID: ").strip()
        if not entity_id.isdigit():
            print("Invalid ID. Must be a number.")
            return

        if entity_type == "category" and int(entity_id) not in valid_ids:
            print(f"No category found with ID {entity_id}.")
            return

        action = input(f"Do you want to 'hide' or 'unhide' the {entity_type}? ").lower().strip()

        if action not in ("hide", "unhide"):
            print("Invalid action.")
            return

        if entity_type == "article":
            response = CategoryService.hide_unhide_article(entity_id, action)
        else:
            response = CategoryService.hide_unhide_category(entity_id, action)

        if response.ok:
            print(f"{entity_type.capitalize()} {action}d successfully.")
        else:
            print(f"Failed to {action} {entity_type}: {response.text}")

    @staticmethod
    def _display_available_categories():
        print("\nAvailable Categories:")
        response = CategoryService.get_categories_for_admin()
        valid_ids = []
        if response.ok:
            categories = response.json().get("data", [])
            if not categories:
                print("No categories found.")
                return valid_ids
            for cat in categories:
                print(f"  ID: {cat['id']} | Name: {cat['name']}")
                valid_ids.append(cat["id"])
        else:
            PrintHelpers.print_error("Failed to fetch categories.")
        return valid_ids
