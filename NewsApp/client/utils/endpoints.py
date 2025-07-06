# ------------------- Base URL -------------------
BASE_URL = "http://localhost:5000"

# ------------------- Auth Endpoints -------------------
LOGIN = "/api/login"
SIGNUP = "/api/signup"

# ------------------- Category Endpoints -------------------
ADD_CATEGORY = "/api/admin/categories"
GET_CATEGORIES = "/api/categories"
GET_CATEGORY_FOR_ADMIN = "/api/admin/categories"

# ------------------- Article Endpoints -------------------
TODAY_HEADLINES = "/api/articles/today"
GET_ARTICLES_BY_RANGE = "/api/articles/range"
SEARCH_ARTICLES = "/api/articles/search"
SAVE_ARTICLE = "/api/articles/{article_id}/save"
UNSAVE_ARTICLE = "/api/articles/{article_id}/unsave"
REPORT_ARTICLE = "/api/article-visibility/report/{article_id}"
READ_HISTORY = "/api/history/{article_id}"
GET_SAVED_ARTICLES = "/api/users/saved-articles"
GET_ALL_ARTICLES = "/api/articles"

# ------------------- Reaction Endpoints -------------------
REACT_TO_ARTICLE = "/api/reactions/{article_id}/{reaction}"
GET_USER_REACTIONS = "/api/reactions"
DELETE_REACTION = "/api/reactions/{article_id}"

# ------------------- Notification Endpoints -------------------
GET_NOTIFICATIONS = "/api/notifications"
GET_NOTIFICATION_PREFERENCES = "/api/notifications/preferences"
UPDATE_NOTIFICATION_PREFERENCES = "/api/notifications/preferences"

# ------------------- User Keyword Endpoints -------------------
ADD_USER_KEYWORD = "/api/user-keywords"
GET_USER_KEYWORDS = "/api/user-keywords"
DELETE_USER_KEYWORD = "/api/user-keywords/{keyword_id}"

# ------------------- Keyword Endpoints -------------------
KEYWORDS = "/api/keywords"

# ------------------- Admin/External Server Endpoints -------------------
GET_EXTERNAL_SERVERS = "/api/admin/external-servers"
UPDATE_EXTERNAL_SERVER = "/api/admin/external-servers"

# ------------------- Blocked Keyword Endpoints -------------------
ADD_BLOCKED_KEYWORD = "/api/article-visibility/blocked-keywords"
GET_BLOCKED_KEYWORDS = "/api/article-visibility/blocked-keywords"
DELETE_BLOCKED_KEYWORD = "/api/article-visibility/blocked-keywords/{keyword_id}"

# ------------------- Report/Moderation Endpoints -------------------
GET_REPORTS = "/api/article-visibility/reports"
HIDE_UNHIDE_ARTICLE = "/api/article-visibility/articles/{article_id}/{action}"
HIDE_UNHIDE_CATEGORY = "/api/article-visibility/categories/{category_id}/{action}"
