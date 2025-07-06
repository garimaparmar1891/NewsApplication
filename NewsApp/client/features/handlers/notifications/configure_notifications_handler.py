from features.services.notifications.configure_notifications_service import NotificationPreferencesService
from features.services.keywords.user_keywords_service import UserKeywordsService
from utils.response_handler import handle_data_response
from constants import messages as msg

class ConfigureNotificationsHandler:
    @staticmethod
    def configure_notifications():
        try:
            
            categories = ConfigureNotificationsHandler._get_categories()
            if not categories:
                return

            preferences = ConfigureNotificationsHandler._get_preferences()
            enabled_ids = ConfigureNotificationsHandler._get_enabled_category_ids(preferences)
            category_map = ConfigureNotificationsHandler._build_category_map(categories)
            
            user_keywords = ConfigureNotificationsHandler._get_user_keywords()
            keywords_by_category = ConfigureNotificationsHandler._organize_keywords_by_category(user_keywords)
            

            ConfigureNotificationsHandler._display_category_status(categories, enabled_ids, keywords_by_category)
            selected_ids = ConfigureNotificationsHandler._get_user_selection()
            
            if not selected_ids:
                return

            user_preferences = ConfigureNotificationsHandler._build_user_preferences(selected_ids, category_map, enabled_ids)
            if not user_preferences:
                return

            response = NotificationPreferencesService.update_preferences(user_preferences)
            ConfigureNotificationsHandler._handle_update_response(response)
            
        except Exception as e:
            print(f"ERROR: Failed to configure notifications: {str(e)}")

    @staticmethod
    def _get_categories():
        try:
            response = NotificationPreferencesService.fetch_categories()
            success, categories = handle_data_response(response, msg.FETCH_CATEGORIES_FAILED)
            
            if not success:
                print(f"ERROR: {categories}")
                return None
                
            if not categories or not isinstance(categories, list):
                print("ERROR: No categories found")
                return None
            
            return categories
            
        except Exception as e:
            print(f"ERROR: Failed to fetch categories: {str(e)}")
            return None

    @staticmethod
    def _get_preferences():
        try:
            response = NotificationPreferencesService.fetch_preferences()
            success, preferences = handle_data_response(response, msg.FETCH_PREFERENCES_FAILED)
            
            if not success:
                print(f"ERROR: {preferences}")
                return []
                
            if not isinstance(preferences, list):
                return []
            
            return preferences
            
        except Exception as e:
            print(f"ERROR: Failed to fetch preferences: {str(e)}")
            return []

    @staticmethod
    def _get_user_keywords():
        try:
            response = UserKeywordsService.view_user_keywords()
            success, keywords = handle_data_response(response, msg.FETCH_USER_KEYWORDS_FAILED)
            
            if not success:
                print(f"WARNING: {keywords}")
                return []
                
            if not isinstance(keywords, list):
                return []
            
            return keywords
            
        except Exception as e:
            print(f"ERROR: Failed to fetch user keywords: {str(e)}")
            return []

    @staticmethod
    def _handle_update_response(response):
        try:
            if response.ok:
                print("Notification preferences updated successfully")
            else:
                error_msg = response.json().get("message", response.text) if response.text else "Unknown error"
                print(f"ERROR: Failed to update notification preferences: {error_msg}")
        except Exception as e:
            print(f"ERROR: Failed to handle update response: {str(e)}")

    @staticmethod
    def _organize_keywords_by_category(user_keywords):
        try:
            keywords_by_category = {}
            for keyword_data in user_keywords:
                if isinstance(keyword_data, dict):
                    category_id = keyword_data.get("category_id") or keyword_data.get("categoryId")
                    keyword = keyword_data.get("word") or keyword_data.get("keyword")
                    if category_id is not None and keyword is not None:
                        if category_id not in keywords_by_category:
                            keywords_by_category[category_id] = []
                        keywords_by_category[category_id].append(keyword)
            return keywords_by_category
        except Exception as e:
            print(f"ERROR: Failed to organize keywords by category: {str(e)}")
            return {}

    @staticmethod
    def _get_enabled_category_ids(preferences):
        try:
            return {pref["categoryId"] for pref in preferences if isinstance(pref, dict) and pref.get("isEnabled", False)}
        except Exception as e:
            print(f"ERROR: Failed to get enabled category IDs: {str(e)}")
            return set()

    @staticmethod
    def _build_category_map(categories):
        try:
            category_map = {}
            for cat in categories:
                if isinstance(cat, dict):
                    cat_id = cat.get("id") or cat.get("Id")
                    cat_name = cat.get("name") or cat.get("Name")
                    if cat_id is not None and cat_name is not None:
                        category_map[cat_id] = cat_name
            return category_map
        except Exception as e:
            print(f"ERROR: Failed to build category map: {str(e)}")
            return {}

    @staticmethod
    def _display_category_status(categories, enabled_ids, keywords_by_category=None):
        try:
            print("\n" + "AVAILABLE CATEGORIES" + "\n" + "="*50)
            
            if not categories:
                print("ERROR: No categories available.")
                return
                
            for category in categories:
                if isinstance(category, dict):
                    cat_id = category.get("id") or category.get("Id")
                    cat_name = category.get("name") or category.get("Name")
                    if cat_id is not None and cat_name is not None:
                        status = "ENABLED" if cat_id in enabled_ids else "DISABLED"
                        print(f"  {cat_id:2d}. {cat_name:<20} - {status}")
                        
                        if keywords_by_category and cat_id in keywords_by_category:
                            keywords = keywords_by_category[cat_id]
                            if keywords:
                                print(f"     Keywords: {', '.join(keywords)}")
            
        except Exception as e:
            print(f"ERROR: Failed to display category status: {str(e)}")

    @staticmethod
    def _get_user_selection():
        try:
            print(msg.CATEGORY_SELECTION_PROMPT)
            user_input = input(msg.CATEGORY_SELECTION_INPUT).strip()
            
            if not user_input:
                return []
                
            # Split by spaces and filter out empty strings
            selected_ids = [id_str.strip() for id_str in user_input.split() if id_str.strip()]
            
            return selected_ids
        except Exception as e:
            print(f"ERROR: Failed to get user selection: {str(e)}")
            return []

    @staticmethod
    def _get_keywords_for_category(category_name, is_enabling):
        try:
            action = "enabling" if is_enabling else "disabling"
            print(f"\nKeywords for '{category_name}' ({action}):")
            print("   Enter keywords separated by commas ")
            print("   Or press Enter to skip keywords for this category")
            keywords_input = input("   Keywords: ").strip()
            
            if not keywords_input:
                return []
                
            keywords = [keyword.strip() for keyword in keywords_input.split(",") if keyword.strip()]
            return keywords
        except Exception as e:
            print(f"ERROR: Failed to get keywords for category: {str(e)}")
            return []

    @staticmethod
    def _build_user_preferences(selected_ids, category_map, enabled_ids):
        try:
            user_preferences = []
            
            for category_id_str in selected_ids:
                category_preference = ConfigureNotificationsHandler._create_category_preference(category_id_str, category_map, enabled_ids)
                if category_preference:
                    user_preferences.append(category_preference)
                    
            return user_preferences
        except Exception as e:
            print(f"ERROR: Failed to build user preferences: {str(e)}")
            return []

    @staticmethod
    def _create_category_preference(category_id_str, category_map, enabled_ids):
        try:
            category_id = int(category_id_str)
            
            if category_id not in category_map:
                print(f"ERROR: Invalid category ID: {category_id} (not found)")
                return None
                
            is_enabled = category_id not in enabled_ids
            category_name = category_map[category_id]
            current_status = "enabled" if category_id in enabled_ids else "disabled"
            new_status = "disabled" if is_enabled else "enabled"
            
            
            keywords = ConfigureNotificationsHandler._get_keywords_for_category(category_name, is_enabled)
            
            return {
                "categoryId": category_id,
                "isEnabled": is_enabled,
                "keywords": keywords
            }
            
        except ValueError:
            print(f"ERROR: Invalid input: '{category_id_str}' is not a valid number")
            return None
        except Exception as e:
            print(f"ERROR: Failed to create category preference: {str(e)}")
            return None
