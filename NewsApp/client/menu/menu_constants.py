# =============================================================================
# MAIN MENU CONSTANTS
# =============================================================================

MAIN_MENU_OPTIONS = [
    "1. Login",
    "2. Signup",
    "3. Exit"
]

MAIN_MENU_SELECT_PROMPT = "Select an option: "
MAIN_MENU_LOGIN_PROMPT = "\nPlease login to continue."
MAIN_MENU_EXIT_MESSAGE = "Exiting. Goodbye!"
MAIN_MENU_INVALID_CHOICE = "Invalid choice. Please try again."

# =============================================================================
# ADMIN MENU CONSTANTS
# =============================================================================

ADMIN_MENU_OPTIONS = [
    "1. View All External Servers",
    "2. View External Server Details",
    "3. Update External Server",
    "4. Add News Category",
    "5. View Reported Articles",
    "6. Manage Keywords (Add/Delete)",
    "7. Hide/Unhide Article",
    "8. Hide/Unhide Category",
    "9. Manage Blocked Keywords (Add/Delete)",
    "10. Logout"
]

ADMIN_MENU_TITLE = "\n=== Admin Menu ==="
ADMIN_MENU_SELECT_PROMPT = "Select an option: "
ADMIN_LOGOUT_SUCCESS = "Admin logged out successfully."
ADMIN_INVALID_CHOICE = "Invalid choice. Please try again."

# =============================================================================
# USER MENU CONSTANTS
# =============================================================================

USER_MENU_OPTIONS = [
    "1. Headlines",
    "2. Saved Article",
    "3. Search Articles",
    "4. View Notifications",
    "5. Logout"
]

USER_MENU_TITLE = "\n=== User Menu ==="
USER_MENU_SELECT_PROMPT = "Select an option: "
USER_MENU_LOGOUT_SUCCESS = "Logged out successfully."
USER_MENU_INVALID_CHOICE = "Invalid choice. Please try again."

# =============================================================================
# HEADLINES MENU CONSTANTS
# =============================================================================

HEADLINES_MENU_OPTIONS = [
    "1. View Today's Headlines",
    "2. View Articles by Date Range and Category",
    "3. Back to Main Menu"
]

HEADLINES_MENU_SELECT_PROMPT = "Select an option: "
HEADLINES_MENU_INVALID_CHOICE = "Invalid choice. Please try again."

# =============================================================================
# KEYWORDS MENU CONSTANTS
# =============================================================================

KEYWORDS_MENU_TITLE = "--- Keyword Management ---"
KEYWORDS_MENU_OPTIONS = [
    "1. Add Keyword",
    "2. Delete Keyword",
    "3. View Keywords",
    "4. Go to Main Menu"
]

# =============================================================================
# BLOCKED KEYWORDS MENU CONSTANTS
# =============================================================================

BLOCKED_KEYWORDS_MENU_OPTIONS = [
    "1. Add Blocked Keyword",
    "2. View Blocked Keywords",
    "3. Delete Blocked Keyword",
    "4. Back to Main Menu"
]

BLOCKED_KEYWORDS_MENU_TITLE = "=== Blocked Keywords Management ==="
BLOCKED_KEYWORDS_MENU_SELECT_PROMPT = "Select an option: "
BLOCKED_KEYWORDS_MENU_RETURN_MESSAGE = "Returning to main menu..."

# =============================================================================
# NOTIFICATION MENU CONSTANTS
# =============================================================================

NOTIFICATION_MENU_TITLE = "=== Notifications Menu==="
NOTIFICATION_MENU_OPTIONS = [
    "1. View Notifications",
    "2. Configure Notifications",
    "3. Add/Delete/View Keywords",
    "4. Back to main menu",
    "5. Logout"
]
NOTIFICATION_MENU_SELECT_PROMPT = "Enter your option: "
NOTIFICATION_MENU_INVALID_CHOICE = "Invalid option"
NOTIFICATION_MENU_LOGOUT_SUCCESS = "Logged out successfully."

# =============================================================================
# USER KEYWORDS MENU CONSTANTS
# =============================================================================

USER_KEYWORDS_MENU_OPTIONS = [
    "1. Add User Keyword",
    "2. View User Keywords",
    "3. Delete User Keyword",
    "4. Back to Main Menu"
]

USER_KEYWORDS_MENU_SELECT_PROMPT = "Select an option: "
USER_KEYWORDS_MENU_INVALID_CHOICE = "Invalid choice. Please try again."

# =============================================================================
# PAGINATED MENU CONSTANTS
# =============================================================================

PAGINATED_MENU_OPTIONS = [
    "1. Read article by ID",
    "2. Save article by ID",
    "3. Next page",
    "4. Previous page",
    "5. Go back to main menu",
    "6. Logout",
    "7. Report article by ID"
]

PAGINATED_MENU_SAVED_OPTIONS = [
    "1. Read article by ID",
    "2. Unsave article by ID",
    "3. Next page",
    "4. Previous page",
    "5. Go back to main menu",
    "6. Logout",
    "7. Report article by ID"
]

PAGINATED_MENU_SELECT_PROMPT = "Enter your choice: "
PAGINATED_MENU_INVALID_CHOICE = "Invalid choice. Please try again."
PAGINATED_MENU_LAST_PAGE = "You are on the last page."
PAGINATED_MENU_FIRST_PAGE = "You are already on the first page."
PAGINATED_MENU_LOGOUT_SUCCESS = "Logged out successfully."
PAGINATED_MENU_ARTICLE_ID_PROMPT = "Enter article ID to {}: "
PAGINATED_MENU_ARTICLE_NOT_FOUND = "Article ID not found."
PAGINATED_MENU_INVALID_INPUT = "Invalid input. Please enter a valid numeric article ID."
PAGINATED_MENU_REPORT_REASON_PROMPT = "Enter reason for reporting this article: "
PAGINATED_MENU_REPORT_REASON_EMPTY = "Report reason cannot be empty."

# =============================================================================
# ARTICLE READING MENU CONSTANTS
# =============================================================================

ARTICLE_READING_OPTIONS = [
    "1. Like this article",
    "2. Dislike this article",
    "3. Save this article",
    "4. Go back to article list",
    "5. Report this article",
    "6. Logout"
]

ARTICLE_READING_SELECT_PROMPT = "\nEnter your choice: "
ARTICLE_READING_INVALID_CHOICE = "Invalid choice. Please try again."
ARTICLE_READING_TITLE = "\n--- Reading Article ---"
ARTICLE_READING_LOGOUT_SUCCESS = "Logged out successfully."
ARTICLE_READING_REPORT_REASON_PROMPT = "Enter reason for reporting this article: "
ARTICLE_READING_REPORT_REASON_EMPTY = "Report reason cannot be empty."

# =============================================================================
# COMMON MENU CONSTANTS
# =============================================================================

RETURN_TO_MAIN_MENU = "Returning to main menu..."
