from datetime import datetime

class DateValidator:
    """Helper class for validating and prompting date input."""

    @staticmethod
    def validate_date_range_input():
        start = DateValidator.prompt_date("Start Date")
        end = DateValidator.prompt_date("End Date")

        if not DateValidator.validate_date_format(start):
            DateValidator.print_invalid_date("Start Date")
            return None, None
        if not DateValidator.validate_date_format(end):
            DateValidator.print_invalid_date("End Date")
            return None, None

        return start, end

    @staticmethod
    def prompt_date(label):
        return input(f"{label} (YYYY-MM-DD): ").strip()

    @staticmethod
    def validate_date_format(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def print_invalid_date(label):
        print(f"Invalid {label.lower()} format.")