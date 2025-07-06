from features.services.admin.categories_service import CategoriesService
from utils.response_handler import handle_response, handle_data_response
from utils.input_utils import get_non_empty_input, get_valid_integer_input, get_valid_action_input
from constants.messages import (
    CATEGORY_NAME_EMPTY,
    CATEGORY_ADD_SUCCESS,
    CATEGORY_ADD_FAILED,
    CATEGORY_INVALID_ID,
    CATEGORY_HIDE_UNHIDE_SUCCESS,
    CATEGORY_HIDE_UNHIDE_FAILED,
    CATEGORY_INVALID_ACTION,
    CATEGORY_ENTER_ID_PROMPT,
    CATEGORY_ACTION_PROMPT,
    CATEGORY_AVAILABLE_TITLE,
    CATEGORY_NO_CATEGORIES_FOUND,
    CATEGORY_FETCH_FAILED,
    CATEGORY_NAME_INPUT_PROMPT,
)

ENTITY_TYPE_CATEGORY = "category"
ENTITY_TYPE_ARTICLE = "article"
ACTION_HIDE = "hide"
ACTION_UNHIDE = "unhide"
CATEGORY_DISPLAY_FORMAT = "  ID: {id} | Name: {name}"


class CategoryHandler:

    @staticmethod
    def add_news_category():
        try:
            category_name = get_non_empty_input(CATEGORY_NAME_INPUT_PROMPT)
            if not category_name:
                print(CATEGORY_NAME_EMPTY)
                return False, CATEGORY_NAME_EMPTY

            response = CategoriesService.add_category(category_name)
            success, message = handle_response(
                response,
                CATEGORY_ADD_SUCCESS.format(name=category_name),
                CATEGORY_ADD_FAILED
            )
            
            if success:
                print(message)
            else:
                print(message)
            return success, message
        except Exception as e:
            error_msg = f"An error occurred while adding category: {str(e)}"
            print(error_msg)
            return False, error_msg

    @staticmethod
    def hide_unhide_article():
        return CategoryHandler._hide_unhide_entity(ENTITY_TYPE_ARTICLE)

    @staticmethod
    def hide_unhide_category():
        return CategoryHandler._hide_unhide_entity(ENTITY_TYPE_CATEGORY)

    @staticmethod
    def get_categories_for_admin():
        try:
            response = CategoriesService.get_categories_for_admin()
            success, data = handle_data_response(response, CATEGORY_FETCH_FAILED)
            
            if success:
                print("Categories fetched successfully")
            else:
                print(str(data))
            return success, data
        except Exception as e:
            error_msg = f"An error occurred while fetching categories: {str(e)}"
            print(error_msg)
            return False, error_msg

    @staticmethod
    def _hide_unhide_entity(entity_type):
        try:
            valid_ids = CategoryHandler._get_valid_category_ids(entity_type)
            entity_id = CategoryHandler._get_entity_id(entity_type, valid_ids)
            if not entity_id:
                print(CATEGORY_INVALID_ID)
                return False, CATEGORY_INVALID_ID

            action = CategoryHandler._get_action(entity_type)
            if not action:
                print(CATEGORY_INVALID_ACTION)
                return False, CATEGORY_INVALID_ACTION

            return CategoryHandler._perform_hide_unhide_action(entity_type, entity_id, action)
        except Exception as e:
            error_msg = f"An error occurred while processing {entity_type} hide/unhide: {str(e)}"
            print(error_msg)
            return False, error_msg

    @staticmethod
    def _get_valid_category_ids(entity_type):
        if entity_type == ENTITY_TYPE_CATEGORY:
            return CategoryHandler._display_available_categories()
        return []

    @staticmethod
    def _get_entity_id(entity_type, valid_ids):
        prompt = CATEGORY_ENTER_ID_PROMPT.format(entity_type=entity_type.capitalize())
        if entity_type == ENTITY_TYPE_CATEGORY:
            return get_valid_integer_input(prompt, valid_ids)
        return get_valid_integer_input(prompt)

    @staticmethod
    def _get_action(entity_type):
        prompt = CATEGORY_ACTION_PROMPT.format(entity_type=entity_type)
        return get_valid_action_input(prompt, (ACTION_HIDE, ACTION_UNHIDE))

    @staticmethod
    def _perform_hide_unhide_action(entity_type, entity_id, action):
        try:
            if entity_type == ENTITY_TYPE_ARTICLE:
                response = CategoriesService.hide_unhide_article(entity_id, action)
            else:
                response = CategoriesService.hide_unhide_category(entity_id, action)

            success, message = handle_response(
                response,
                CATEGORY_HIDE_UNHIDE_SUCCESS.format(entity_type=entity_type.capitalize(), action=action),
                CATEGORY_HIDE_UNHIDE_FAILED.format(action=action, entity_type=entity_type, error="{error}")
            )
            
            if success:
                print(message)
            else:
                print(message)
            return success, message
        except Exception as e:
            error_msg = f"An error occurred while {action}ing {entity_type}: {str(e)}"
            print(error_msg)
            return False, error_msg

    @staticmethod
    def _display_available_categories():
        try:
            print(f"\n{CATEGORY_AVAILABLE_TITLE}")
            response = CategoriesService.get_categories_for_admin()
            valid_ids = []
            
            success, data = handle_data_response(response, CATEGORY_FETCH_FAILED)
            if success and isinstance(data, list):
                if not data:
                    print(CATEGORY_NO_CATEGORIES_FOUND)
                    return valid_ids
                    
                for cat in data:
                    cat_id = cat.get("id") or cat.get("Id")
                    cat_name = cat.get("name") or cat.get("Name")
                    if cat_id is not None and cat_name is not None:
                        print(CATEGORY_DISPLAY_FORMAT.format(id=cat_id, name=cat_name))
                        valid_ids.append(cat_id)
            else:
                print(str(data))
                
            return valid_ids
        except Exception as e:
            error_msg = f"An error occurred while displaying categories: {str(e)}"
            print(error_msg)
            return []
