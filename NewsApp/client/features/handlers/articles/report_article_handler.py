from constants import messages as msg
from features.services.articles.report_article_service import ReportArticleService
from utils.response_handler import handle_response
from utils.input_utils import get_article_id_input

REPORT_OPERATION = "report"

class ReportArticleHandler:

    @staticmethod
    def report_article():
        try:
            print(msg.REPORT_ARTICLE_TITLE)
            
            try:
                article_id = get_article_id_input(REPORT_OPERATION)
            except ValueError:
                print("Invalid article ID format. Please enter a valid number.")
                return False
            except Exception:
                print("Failed to get article ID input.")
                return False
            
            try:
                reason = input(msg.REPORT_REASON_PROMPT).strip()
                if not reason:
                    print(msg.REPORT_REASON_EMPTY)
                    return False
            except Exception:
                print("Failed to get report reason input.")
                return False
            
            try:
                response = ReportArticleService.report_article(article_id, reason)
                success, message = handle_response(response, msg.ARTICLE_REPORT_SUCCESS, msg.ARTICLE_REPORT_FAILED)
                
                if success:
                    print(message)
                else:
                    print(message)
                
                return success
                
            except Exception:
                print("Failed to report article. Please try again later.")
                return False
                
        except Exception:
            print("An unexpected error occurred while reporting the article.")
            return False
