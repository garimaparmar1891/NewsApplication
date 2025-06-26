from datetime import datetime

def validate_date_range_input():
    start = prompt_date("Start Date")
    end = prompt_date("End Date")

    if not validate_date_format(start):
        print_invalid_date("Start Date")
        return None, None
    if not validate_date_format(end):
        print_invalid_date("End Date")
        return None, None

    return start, end

def prompt_date(label):
    return input(f"{label} (YYYY-MM-DD): ").strip()

def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def print_invalid_date(label):
    print(f"Invalid {label.lower()} format.")
