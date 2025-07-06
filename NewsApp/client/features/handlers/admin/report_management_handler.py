from features.services.admin.report_management_manager import ReportManagementManager
from utils.response_handler import handle_data_response
from constants.messages import (
    ARTICLES_FETCH_FAILED, 
    NO_REPORTED_ARTICLES_FOUND, 
    REPORTED_ARTICLES_TITLE,
    REPORTED_ARTICLES_FETCH_FAILED
)

class ReportManagementHandler:

    @staticmethod
    def view_reported_articles():
        try:
            response = ReportManagementManager.fetch_reported_articles()
            success, data = handle_data_response(response, ARTICLES_FETCH_FAILED)
            
            if not success:
                print(REPORTED_ARTICLES_FETCH_FAILED.format(error=data))
                return False, data
                
            ReportManagementHandler._print_reported_articles(data)
            return True, data
            
        except Exception as e:
            error_message = REPORTED_ARTICLES_FETCH_FAILED.format(error=str(e))
            print(error_message)
            return False, error_message

    @staticmethod
    def _print_reported_articles(reports):
        try:
            if not reports:
                print(NO_REPORTED_ARTICLES_FOUND)
                return
                
            print(REPORTED_ARTICLES_TITLE)
            for report in reports:
                ReportManagementHandler._print_single_report(report)
                print("-" * 50)
        except Exception:
            pass

    @staticmethod
    def _print_single_report(report):
        try:
            print(f"Article ID: {report.get('ArticleId', 'N/A')}")
            print(f"Reported By: {report.get('Username', 'N/A')}")
            print(f"Email: {report.get('Email', 'N/A')}")
            print(f"Reason: {report.get('Reason', 'N/A')}")
        except Exception:
            pass
