# === Auth Messages ===
USER_ALREADY_EXISTS = "User already exists"
USER_REGISTERED = "User registered successfully"
INVALID_CREDENTIALS = "Invalid credentials"
INVALID_EMAIL_FORMAT = "Invalid email format. Please provide a valid email address."
REQUIRED_SIGNUP_FIELDS = ["username", "email", "password"]
REQUIRED_LOGIN_FIELDS = ["email", "password"]
UNAUTHORIZED = "Unauthorized"

# === General Messages ===
MISSING_REQUIRED_FIELDS = "Missing required fields"
INVALID_INPUT = "Invalid input"
FORBIDDEN = "Forbidden"
INTERNAL_SERVER_ERROR = "An unexpected error occurred"

# === External Server Messages ===
EXTERNAL_SERVER_UPDATED = "External server updated successfully"
EXTERNAL_SERVER_UPDATE_FAILED = "Failed to update external server"
EXTERNAL_SERVER_ADDED = "External server added successfully"
EXTERNAL_SERVER_ADD_FAILED = "Failed to add external server"

# === Category Messages ===
CATEGORY_NAME_REQUIRED = "Category name is required"
CATEGORY_ADDED = "Category added successfully"
CATEGORY_ADD_FAILED = "Failed to add category"

# === Article Messages ===
ARTICLE_SAVED = "Article saved successfully"
ARTICLE_SAVE_FAILED = "Failed to save article"
ARTICLE_NOT_FOUND = "Article not found"
ARTICLE_UNSAVED_SUCCESS = "Article unsaved successfully"
ARTICLE_UNSAVE_FAILED = "Could not unsave article"
ARTICLE_NOT_SAVED = "This article is not in your saved articles list"
ARTICLE_HIDDEN_ERROR = "Cannot save a hidden article."
NO_HEADLINES_AVAILABLE = "No headlines available"
NO_ARTICLES_FOUND = "No articles found"
NO_ARTICLES_FOR_KEYWORD = "No articles found for the keyword"
FAILED_TO_RECORD_READ_HISTORY = "Failed to store read history"
NO_SAVED_ARTICLES = "No saved articles found"

# === Search & Filter Messages ===
MISSING_DATE_RANGE = "Missing required parameters: start_date and end_date"
MISSING_SEARCH_PARAMS = "Missing required parameters: q, start_date, end_date"

# === Keyword Messages ===
MISSING_KEYWORD_FIELDS = "Keyword and category_id are required"
KEYWORD_ADDED = "Keyword added successfully"
KEYWORD_ADD_FAILED = "Keyword already exists or failed to add"
KEYWORD_DELETED = "Keyword deleted successfully"
KEYWORD_NOT_FOUND = "Keyword not found"

# === Notification & Preferences ===
PREFERENCES_UPDATED = "Preferences and keywords updated successfully"
PREFERENCES_UPDATE_FAILED = "Failed to update preferences"
INVALID_PREFERENCE_FORMAT = "Invalid input format. 'categories' must be a list."
EMAIL_SENT_SUCCESS = "Email sent successfully"
EMAIL_SEND_FAILED = "Failed to send email"
NO_NOTIFICATIONS = "No notifications found"
NO_MATCHING_ARTICLES = "No matching articles"
NO_ENABLED_CATEGORIES = "No enabled categories"
EMAIL_DISPATCH_SUCCESS = "Sent {count} article(s)"

# === User Messages ===
USER_NOT_FOUND = "User not found"
INVALID_USER_ID = "Invalid user ID"

# === Report Article Threshold ===
REPORT_THRESHOLD = 2

CATEGORY_ALREADY_EXISTS = "Category already exists with the same name."

READ_RECORDED = "Read recorded successfully."
READ_RECORD_FAILED = "Failed to record read history."
INVALID_DATE_RANGE = "Start date cannot be after end date."
INVALID_DATE_FORMAT = "Invalid date format. Expected YYYY-MM-DD."
NO_ARTICLES_IN_RANGE = "No articles found in the specified date range"

# === Article Reaction Messages ===
INVALID_REACTION_TYPE = "Invalid reaction type."
REACTION_RECORDED = "Reaction recorded successfully."
REACTION_FAILED = "Failed to record reaction."
ALREADY_LIKED = "You already liked this article."
ALREADY_DISLIKED = "You already disliked this article."

# === Article Visibility Messages ===
ARTICLE_REPORTED_SUCCESS = "Article reported successfully."
ARTICLE_HIDDEN_SUCCESS = "Article hidden successfully."
ARTICLE_UNHIDDEN_SUCCESS = "Article unhidden successfully."
CATEGORY_HIDDEN_SUCCESS = "Category hidden successfully."
CATEGORY_UNHIDDEN_SUCCESS = "Category unhidden successfully."
BLOCKED_KEYWORD_ADDED = "Blocked keyword added successfully."
BLOCKED_KEYWORD_DELETED = "Blocked keyword deleted and related articles unhidden."
INVALID_VISIBILITY_ACTION = "Invalid action. Use 'hide' or 'unhide'"
KEYWORD_REQUIRED = "Keyword is required"
REPORT_FIELDS_REQUIRED = "Article ID, User ID, and Reason are required"
ARTICLE_OR_USER_NOT_FOUND = "Article or User not found"

# === Database Error Messages ===
DB_ERROR_CREATE_USER = "[DB ERROR] create_user"
DB_ERROR_GET_ADMIN_EMAIL = "[DB ERROR] get_admin_email"
DB_ERROR_GET_EXTERNAL_SERVERS = "[DB ERROR] get_external_servers"
DB_ERROR_GET_EXTERNAL_SERVER_KEYS = "[DB ERROR] get_external_server_keys"
DB_ERROR_UPDATE_EXTERNAL_SERVER = "[DB ERROR] update_external_server"
DB_ERROR_GET_CATEGORIES = "[DB ERROR] get_categories"
DB_ERROR_GET_CATEGORY_BY_NAME = "[DB ERROR] get_category_by_name"
DB_ERROR_ADD_CATEGORY = "[DB ERROR] add_category"
DB_ERROR_GET_KEYWORDS = "[DB ERROR] get_keywords"
DB_ERROR_ADD_KEYWORD = "[DB ERROR] add_keyword"
DB_ERROR_DELETE_KEYWORD = "[DB ERROR] delete_keyword"
DB_ERROR_REACT_TO_ARTICLE = "[DB ERROR] react_to_article"
DB_ERROR_GET_USER_REACTIONS = "[DB ERROR] get_user_reactions"
DB_ERROR_GET_TODAY_HEADLINES = "[DB ERROR] get_today_headlines"
DB_ERROR_SEARCH_ARTICLES = "[DB ERROR] search_articles_by_keyword_and_range"
DB_ERROR_GET_ARTICLES_BY_RANGE = "[DB ERROR] get_articles_by_range"
DB_ERROR_GET_ALL_ARTICLES = "[DB ERROR] get_all_articles"
DB_ERROR_GET_ARTICLE_BY_ID = "[DB ERROR] get_article_by_id"
DB_ERROR_GET_READ_HISTORY = "[DB ERROR] get_read_history"
DB_ERROR_GET_BLOCKED_KEYWORDS = "[DB ERROR] get_blocked_keywords"
DB_ERROR_INSERT_READ_HISTORY = "[DB ERROR] insert_read_history"
DB_ERROR_BULK_INSERT_ARTICLE = "[Bulk Insert Error]"
DB_ERROR_COULD_NOT_FETCH_ID = "Could not fetch inserted article ID for"
DB_ERROR_ADD_REPORT = "[DB ERROR] add_report"
DB_ERROR_GET_REPORTED_ARTICLES = "[DB ERROR] get_all_reported_articles"
DB_ERROR_GET_REPORT_COUNT = "[DB ERROR] get_report_count"
DB_ERROR_HIDE_ARTICLE = "[DB ERROR] hide_article"
DB_ERROR_UNHIDE_ARTICLE = "[DB ERROR] unhide_article"
DB_ERROR_HIDE_CATEGORY = "[DB ERROR] hide_category"
DB_ERROR_UNHIDE_CATEGORY = "[DB ERROR] unhide_category"
DB_ERROR_ADD_BLOCKED_KEYWORD = "[DB ERROR] add_blocked_keyword"
DB_ERROR_CLEAR_REPORTS = "[DB ERROR] clear_article_reports"
DB_ERROR_DELETE_BLOCKED_KEYWORD = "[DB ERROR] delete_blocked_keyword"
DB_ERROR_GET_USER_REPORTED = "[DB ERROR] get_user_reported_articles"
DB_ERROR_RECORD_LOGIN = "[DB ERROR] record_login"
DB_ERROR_SAVE_ARTICLE = "[DB ERROR] save_article"
DB_ERROR_UNSAVE_ARTICLE = "[DB ERROR] unsave_article"
DB_ERROR_GET_SAVED_ARTICLES = "[DB ERROR] get_saved_articles"
DB_ERROR_GET_VISIBLE_ARTICLE_IDS = "[DB ERROR] get_visible_article_ids"
DB_ERROR_GET_SAVED_ARTICLE_IDS = "[DB ERROR] get_saved_article_ids"

DB_ERROR_UPDATE_PREFERENCES = "[DB ERROR] update_user_preferences"
DB_ERROR_GET_ENABLED_CATEGORIES = "[DB ERROR] get_enabled_category_ids"
DB_ERROR_GET_USER_PREFERENCES = "[DB ERROR] get_user_preferences"
DB_ERROR_GET_USER_KEYWORDS = "[DB ERROR] get_user_keywords"
DB_ERROR_ADD_USER_KEYWORD = "[DB ERROR] add_user_keyword"
DB_ERROR_DELETE_USER_KEYWORD = "[DB ERROR] delete_user_keyword"
DB_ERROR_GET_USER_KEYWORD_MAP = "[DB ERROR] get_user_keywords_map"
DB_ERROR_GET_UNSENT_ARTICLES = "[DB ERROR] get_unsent_articles"
DB_ERROR_GET_ARTICLES_BY_CATEGORIES = "[DB ERROR] get_articles_by_categories"
DB_ERROR_MARK_ARTICLES_SENT = "[DB ERROR] mark_articles_as_sent"
DB_ERROR_GET_UNREAD_NOTIFICATIONS = "[DB ERROR] get_unread_user_notifications"
DB_ERROR_MARK_NOTIFICATIONS_READ = "[DB ERROR] mark_notifications_as_read"
DB_ERROR_INSERT_NOTIFICATION = "[DB ERROR] insert_notification"
DB_ERROR_GET_USERS_WITH_PREFS = "[DB ERROR] get_users_with_enabled_preferences"
DB_ERROR_GET_LAST_LOGIN = "[DB ERROR] get_last_login"
DB_ERROR_FETCH_COLUMN = "[DB ERROR] _fetch_column"

# === NewsAPI Handler Messages ===
NEWSAPI_REQUESTING_ARTICLES = "Requesting NewsAPI articles for category: {category}"
NEWSAPI_REQUEST_URL = "URL: {url}"
NEWSAPI_ERROR_FETCHING = "Error fetching from NewsAPI: {error}"
NEWSAPI_ERROR_RESPONSE = "NewsAPI Error {status_code}: {response_text}"
THENEWSAPI_ERROR_FETCHING = "Error fetching from TheNewsAPI: {error}"

# === External News Service Messages ===
FETCHING_FROM_SOURCE = "Fetching articles from {name}"
INSERTED_ARTICLES_FROM_SOURCE = "Inserted {count} new articles from {name}"
SENT_EMAIL_NOTIFICATIONS = "Sent {count} article notifications to {email}"
ERROR_FETCHING_FROM_SOURCE = "Error fetching articles from {name}: {error}"
ERROR_IN_SEND_NOTIFICATIONS = "Error in _send_notifications_for_user: {error}"
