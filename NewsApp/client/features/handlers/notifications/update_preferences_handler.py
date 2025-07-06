from features.services.notifications.preferences_service import PreferencesService
from constants.messages import (
    UPDATE_PREFERENCES_TITLE,
    ENTER_CATEGORY_ID_PROMPT,
    ENABLE_NOTIFICATIONS_PROMPT,
    PREFERENCES_UPDATE_SUCCESS,
    PREFERENCES_UPDATE_FAILED,
    INVALID_CATEGORY_ID_ERROR,
    INVALID_INPUT_ERROR
)

class UpdatePreferencesHandler:
    @staticmethod
    def update_preferences():
        try:
            print(UPDATE_PREFERENCES_TITLE)
            
            category_id = UpdatePreferencesHandler._get_category_id()
            if category_id is None:
                return
                
            is_enabled = UpdatePreferencesHandler._get_enabled_status()
            if is_enabled is None:
                return
            
            preferences = {
                "preferences": [
                    {"categoryId": category_id, "isEnabled": is_enabled}
                ]
            }
            
            response = PreferencesService.send_update_preferences_request(preferences)
            UpdatePreferencesHandler._handle_response(response)
            
        except Exception:
            pass

    @staticmethod
    def _get_category_id():
        try:
            user_input = input(ENTER_CATEGORY_ID_PROMPT).strip()
            if not user_input:
                print("Category ID cannot be empty.")
                return None
            return int(user_input)
        except ValueError:
            print(INVALID_CATEGORY_ID_ERROR.format("Category ID"))
            return None
        except Exception:
            return None

    @staticmethod
    def _get_enabled_status():
        try:
            user_input = input(ENABLE_NOTIFICATIONS_PROMPT).strip().lower()
            if not user_input:
                print("Please provide a response (yes/no).")
                return None
            if user_input not in ("yes", "no"):
                print(INVALID_INPUT_ERROR.format("Input"))
                return None
            return user_input == "yes"
        except Exception:
            return None

    @staticmethod
    def _handle_response(response):
        try:
            if response.ok:
                print(PREFERENCES_UPDATE_SUCCESS)
            else:
                error_msg = response.json().get("message", response.text)
                print(PREFERENCES_UPDATE_FAILED.format(error_msg))
        except Exception:
            pass
