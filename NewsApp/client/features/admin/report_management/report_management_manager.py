from features.admin.report_management.report_management_service import ReportManagementService
from features.admin.utils.print_helpers import PrintHelpers

class ReportManagementManager:
    """Handles user interaction for viewing reported articles."""

    @staticmethod
    def view_reported_articles():
        reports = ReportManagementService.get_reported_articles()
        if reports is None:
            print("Failed to fetch reports.")
            return
        PrintHelpers.print_reported_articles(reports) 