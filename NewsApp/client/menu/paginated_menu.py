from utils.paginated_menu_utils import PaginatedMenuUtils
from .menu_constants import (
    PAGINATED_MENU_OPTIONS,
    PAGINATED_MENU_SAVED_OPTIONS,
    PAGINATED_MENU_SELECT_PROMPT,
    PAGINATED_MENU_INVALID_CHOICE,
    PAGINATED_MENU_LAST_PAGE,
    PAGINATED_MENU_FIRST_PAGE
)

ITEMS_PER_PAGE = 5


class PaginatedMenu:

    def __init__(self, articles, context_label="Articles", is_saved_articles=False, refresh_callback=None):
        self.articles = articles
        self.context_label = context_label
        self.is_saved_articles = is_saved_articles
        self.refresh_callback = refresh_callback
        
        self.current_page = 0
        self.total_pages = PaginatedMenuUtils.calculate_total_pages(articles, ITEMS_PER_PAGE)
        
        self.menu_options = PAGINATED_MENU_SAVED_OPTIONS if is_saved_articles else PAGINATED_MENU_OPTIONS

    def show(self):
        while True:
            PaginatedMenuUtils.show_header()
            
            current_articles = PaginatedMenuUtils.get_current_page_articles(
                self.articles, self.current_page, ITEMS_PER_PAGE
            )
            PaginatedMenuUtils.show_articles(current_articles, self.context_label)
            PaginatedMenuUtils.show_page_info(self.current_page, self.total_pages)
            PaginatedMenuUtils.show_menu_options(self.menu_options)
            
            choice = PaginatedMenuUtils.get_user_choice(PAGINATED_MENU_SELECT_PROMPT)
            if self._handle_menu_choice(choice):
                break

    def _handle_menu_choice(self, choice):
        if choice == "1":
            PaginatedMenuUtils.read_article(self.articles)
        elif choice == "2":
            new_articles = PaginatedMenuUtils.save_unsave_article(self.is_saved_articles, self.refresh_callback)
            if new_articles:
                self._update_articles(new_articles)
        elif choice == "3":
            if PaginatedMenuUtils.can_go_next_page(self.current_page, self.total_pages):
                self.current_page += 1
            else:
                PaginatedMenuUtils.show_message(PAGINATED_MENU_LAST_PAGE)
        elif choice == "4":
            if PaginatedMenuUtils.can_go_previous_page(self.current_page):
                self.current_page -= 1
            else:
                PaginatedMenuUtils.show_message(PAGINATED_MENU_FIRST_PAGE)
        elif choice == "5":
            PaginatedMenuUtils.return_to_main_menu()
            return True
        elif choice == "6":
            PaginatedMenuUtils.logout()
            exit()
        elif choice == "7":
            PaginatedMenuUtils.report_article()
        else:
            PaginatedMenuUtils.show_message(PAGINATED_MENU_INVALID_CHOICE)
        
        return False

    def _update_articles(self, new_articles):
        self.articles = new_articles
        self.total_pages = PaginatedMenuUtils.calculate_total_pages(new_articles, ITEMS_PER_PAGE)
        self.current_page = PaginatedMenuUtils.adjust_page_if_needed(self.current_page, self.total_pages)
