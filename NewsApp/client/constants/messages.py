# =============================================================================
# EXTERNAL SERVER MESSAGES
# =============================================================================
EXTERNAL_SERVER_FETCH_FAILED = "Failed to fetch servers: {}"
EXTERNAL_SERVER_UPDATE_SUCCESS = "External server updated successfully."
EXTERNAL_SERVER_UPDATE_FAILED = "Failed to update server: {}"
EXTERNAL_SERVER_INVALID_ID = "Invalid server ID."
EXTERNAL_SERVER_NO_UPDATE_FIELDS = "No fields provided to update."
EXTERNAL_SERVER_NO_SERVERS_FOUND = "No external servers found."

SERVER_FIELDS = {
    "name": "Name",
    "base_url": "Base_Url",
    "api_key": "Api_key",
    "is_active": "Is_Active"
}

EXTERNAL_SERVER_LIST_TITLE = "\n--- External Servers List ---"
EXTERNAL_SERVER_DETAILS_TITLE = "\n--- View External Server Details ---"
EXTERNAL_SERVER_EDIT_TITLE = "\n--- Edit External Server ---"
EXTERNAL_SERVER_AVAILABLE_TITLE = "\nAvailable External Servers:"
EXTERNAL_SERVER_ID_PROMPT = "Enter External Server ID to update: "
EXTERNAL_SERVER_NAME_PROMPT = "Enter new server name (or press Enter to skip): "
EXTERNAL_SERVER_URL_PROMPT = "Enter new server URL (or press Enter to skip): "
EXTERNAL_SERVER_API_KEY_PROMPT = "Enter new API key (or press Enter to skip): "
EXTERNAL_SERVER_ISACTIVE_PROMPT = "Enter new active status (1 for active, 0 for inactive, or press Enter to skip): "


# =============================================================================
# BLOCKED KEYWORDS MESSAGES
# =============================================================================
BLOCKED_KEYWORD_EMPTY = "Keyword cannot be empty."
BLOCKED_KEYWORD_SUCCESS = "Keyword '{keyword}' blocked successfully."
BLOCKED_KEYWORD_FETCH_FAILED = "Failed to fetch blocked keywords."
BLOCKED_KEYWORD_BLOCK_FAILED = "Failed to block keyword: {error}"
BLOCKED_KEYWORD_LIST_EMPTY = "No blocked keywords found."
BLOCKED_KEYWORD_DELETE_SUCCESS = "Blocked keyword deleted successfully."
BLOCKED_KEYWORD_DELETE_FAILED = "Failed to delete blocked keyword: {error}"
BLOCKED_KEYWORD_INVALID_ID = "Invalid keyword ID. Please enter a number."
BLOCKED_KEYWORD_DELETE_PROMPT = "Enter the ID of the blocked keyword to delete: "


# =============================================================================
# GENERIC ERROR MESSAGES
# =============================================================================
UNKNOWN_ERROR = "Unknown error occurred"


# =============================================================================
# KEYWORD MANAGEMENT MESSAGES
# =============================================================================
ADD_KEYWORD_TITLE = "Add Keyword"
DELETE_KEYWORD_TITLE = "Delete Keyword"
ENTER_CATEGORY_ID_PROMPT = "Enter Category ID to assign the keyword: "
ENTER_KEYWORD_ADD_PROMPT = "Enter keyword to add: "
ENTER_KEYWORD_DELETE_PROMPT = "Enter keyword to delete: "
INVALID_CATEGORY_ID = "Invalid category ID. Must be a number."
KEYWORD_ADD_SUCCESS = "Keyword added successfully."
KEYWORD_ADD_FAILED = "Failed to add keyword."
KEYWORD_DELETE_SUCCESS = "Keyword deleted successfully."
KEYWORD_DELETE_FAILED = "Failed to delete keyword."

FETCH_CATEGORIES_FAILED = "Failed to fetch categories."
NO_CATEGORIES_FOUND = "No categories available. Please add a category first."

VIEW_KEYWORDS_TITLE = "View Keywords"
FETCH_KEYWORDS_FAILED = "Failed to fetch keywords."
NO_KEYWORDS_FOUND = "No keywords found."

CATEGORIES_AVAILABLE_TITLE = "Available Categories:"
KEYWORDS_AVAILABLE_TITLE = "Available Keywords:"


# =============================================================================
# CATEGORY MANAGEMENT MESSAGES
# =============================================================================
CATEGORY_NAME_EMPTY = "Category name cannot be empty."
CATEGORY_ADD_SUCCESS = "Category '{name}' added successfully."
CATEGORY_ADD_FAILED = "Failed to add category: {error}"
CATEGORY_INVALID_ID = "Invalid ID. Must be a number."
CATEGORY_NOT_FOUND = "No category found with ID {id}."
CATEGORY_HIDE_UNHIDE_SUCCESS = "{entity_type} {action}d successfully."
CATEGORY_HIDE_UNHIDE_FAILED = "Failed to {action} {entity_type}: {error}"
CATEGORY_INVALID_ACTION = "Invalid action."
CATEGORY_ENTER_ID_PROMPT = "Enter {entity_type} ID: "
CATEGORY_ACTION_PROMPT = "Do you want to 'hide' or 'unhide' the {entity_type}? "
CATEGORY_AVAILABLE_TITLE = "Available Categories:"
CATEGORY_NO_CATEGORIES_FOUND = "No categories found."
CATEGORY_FETCH_FAILED = "Failed to fetch categories: {error}"
CATEGORY_NAME_INPUT_PROMPT = "Enter new category name: "


# =============================================================================
# ARTICLE MESSAGES
# =============================================================================
ARTICLES_FETCH_FAILED = "Failed to fetch articles. Please try again later."
TODAY_HEADLINES_FETCH_FAILED = "Failed to fetch today's headlines. Please try again later."

# Article Save/Unsave Messages
SAVE_ARTICLE_TITLE = "\n--- Save Article ---"
UNSAVE_ARTICLE_TITLE = "\n--- Unsave Article ---"
ARTICLE_SAVE_SUCCESS = "Article saved successfully."
ARTICLE_SAVE_FAILED = "Failed to save article: {error}"
ARTICLE_UNSAVE_SUCCESS = "Article unsaved successfully."
ARTICLE_UNSAVE_FAILED = "Failed to unsave article: {error}"

# Article Report Messages
REPORT_ARTICLE_TITLE = "\n--- Report Article ---"
ARTICLE_REPORT_SUCCESS = "Article reported successfully."
ARTICLE_REPORT_FAILED = "Failed to report article: {error}"
REPORT_REASON_PROMPT = "Enter reason for reporting this article: "
REPORT_REASON_EMPTY = "Report reason cannot be empty."

# Search Messages
SEARCH_FAILED = "Failed to search articles"
SEARCH_TITLE = "\n--- Search Articles ---"
SEARCH_NO_RESULTS = "No articles found for the given criteria."

# Saved Articles Messages
SAVED_ARTICLES_FETCH_FAILED = "Failed to fetch saved articles: {error}"

# Report Management Messages
NO_REPORTED_ARTICLES_FOUND = "No reported articles found."
REPORTED_ARTICLES_TITLE = "\n--- Reported Articles ---"
REPORTED_ARTICLES_FETCH_FAILED = "Failed to fetch reported articles: {error}"


# =============================================================================
# AUTHENTICATION MESSAGES
# =============================================================================
LOGIN_FAILED = "Login failed: {}"

SIGNUP_SUCCESS = "Signup successful. Please Login!"
SIGNUP_FAILED = "Signup failed: {error}"


# =============================================================================
# NOTIFICATION KEYWORDS MESSAGES
# =============================================================================
NOTIFICATION_KEYWORDS_MANAGEMENT_TITLE = "\n--- Notification Keywords Management ---"
NOTIFICATION_KEYWORDS_ADD_TITLE = "\n--- Add Notification Keyword ---"
NOTIFICATION_KEYWORDS_VIEW_TITLE = "\n--- Notification Keywords ---"
NOTIFICATION_KEYWORDS_DELETE_TITLE = "\n--- Delete Notification Keyword ---"
NOTIFICATION_KEYWORDS_ADD_OPTION = "1. Add Notification Keyword"
NOTIFICATION_KEYWORDS_VIEW_OPTION = "2. View Notification Keywords"
NOTIFICATION_KEYWORDS_DELETE_OPTION = "3. Delete Notification Keyword"
NOTIFICATION_KEYWORDS_BACK_OPTION = "4. Back to Notifications"
NOTIFICATION_KEYWORDS_SELECT_PROMPT = "Select an option: "
NOTIFICATION_KEYWORDS_INVALID_OPTION = "Invalid option. Please try again."
NOTIFICATION_KEYWORDS_KEYWORD_PROMPT = "Enter keyword to be notified about: "
NOTIFICATION_KEYWORDS_CATEGORY_PROMPT = "Enter category (optional, press Enter to skip): "
NOTIFICATION_KEYWORDS_DELETE_ID_PROMPT = "Enter the ID of the keyword to delete: "
NOTIFICATION_KEYWORDS_DISPLAY_FORMAT = "[{idx}] Keyword: {keyword}, Category: {category}"
NOTIFICATION_KEYWORDS_ADD_ERROR = "Failed to add notification keyword: {}"
NOTIFICATION_KEYWORDS_DELETE_ERROR = "Failed to delete notification keyword: {}"
NOTIFICATION_KEYWORDS_FETCH_ERROR = "Failed to fetch notification keywords: {}"
NOTIFICATION_KEYWORDS_INVALID_FORMAT = "Invalid data format received from server."


# =============================================================================
# USER KEYWORDS MESSAGES
# =============================================================================
USER_KEYWORDS_MANAGEMENT_TITLE = "\n--- User Keywords Management ---"
USER_KEYWORDS_ADD_TITLE = "\n--- Add User Keyword ---"
USER_KEYWORDS_DELETE_TITLE = "\n--- Delete User Keyword ---"
USER_KEYWORDS_KEYWORD_PROMPT = "Enter a keyword to track: "
USER_KEYWORDS_DISPLAY_FORMAT = "[{id} | Keyword: {keyword}"


# =============================================================================
# NOTIFICATION PREFERENCES MESSAGES
# =============================================================================
FETCH_PREFERENCES_FAILED = "Failed to fetch preferences"
FETCH_USER_KEYWORDS_FAILED = "Failed to fetch user keywords"
NO_VALID_CHANGES = "No valid changes to update."
INVALID_CATEGORY_ID_ERROR = "Invalid category ID: {}"
INVALID_INPUT_ERROR = "Invalid input: {} is not a valid number."
CATEGORY_SELECTION_PROMPT = "\n" + "-"*50 + "\nEnter category IDs to toggle (e.g., 1 3 5), or press Enter to skip:"
CATEGORY_SELECTION_INPUT = "Your selection: "

# Update Preferences Messages
UPDATE_PREFERENCES_TITLE = "\n--- Update Notification Preferences ---"
ENTER_CATEGORY_ID_PROMPT = "Enter Category ID: "
ENABLE_NOTIFICATIONS_PROMPT = "Enable notifications for this category? (yes/no): "
PREFERENCES_UPDATE_SUCCESS = "Preferences updated successfully."
PREFERENCES_UPDATE_FAILED = "Failed to update preferences: {}"

# Notification Messages
NO_NOTIFICATIONS_FOUND = "No new notification found!"
NOTIFICATIONS_FETCH_FAILED = "Failed to fetch notifications: {}"
NOTIFICATIONS_FETCH_SUCCESS = "Notifications fetched successfully."


# =============================================================================
# ARTICLE REACTIONS MESSAGES
# =============================================================================
REACT_TO_ARTICLE_TITLE = "\n--- React to Article ---"
USER_REACTIONS_TITLE = "\n--- Your Article Reactions ---"
REMOVE_REACTION_TITLE = "\n--- Remove Reaction ---"
REACTION_INVALID = "Invalid reaction. Please enter 'like' or 'dislike'."
REACTION_SUCCESS = "Reaction recorded successfully!"
REACTION_PROMPT = "Enter your reaction (like/dislike): "
REACTION_FAILED = "Failed to react: {}"
REACTIONS_FETCH_FAILED = "Could not fetch reactions: {}"
NO_REACTIONS_FOUND = "You haven't reacted to any articles yet."
REACTION_REMOVED = "Reaction removed."
REACTION_REMOVE_FAILED = "Failed to remove reaction: {}"
REACTION_DISPLAY_FORMAT = "Reaction {idx}:\nArticle ID : {article_id}\nReaction   : {reaction}\nReacted At : {reacted_at}"


# =============================================================================
# INPUT UTILITY MESSAGES
# =============================================================================
INPUT_CANNOT_BE_EMPTY = "Input cannot be empty. Please try again."
PLEASE_ENTER_VALID_NUMBER = "Please enter a valid number."
PLEASE_ENTER_VALID_ID = "Please enter a valid ID from the list."
PLEASE_ENTER_VALID_ACTION = "Please enter one of: {}"
ENTER_ARTICLE_ID_PROMPT = "Enter Article ID to {}: "
ENTER_KEYWORD_PROMPT = "Enter keyword: "
ENTER_START_DATE_PROMPT = "Enter start date (YYYY-MM-DD): "
ENTER_END_DATE_PROMPT = "Enter end date (YYYY-MM-DD): "
