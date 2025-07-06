from utils.http_client import HttpClient
from constants import messages as msg

def handle_response(response, success_message, error_message):
    if response.ok:
        return True, success_message
    error = HttpClient.safe_json_get(response, "error", msg.UNKNOWN_ERROR)
    return False, error_message.format(error=error)

def handle_data_response(response, error_message):
    if response.ok:
        data = HttpClient.safe_extract_data(response, [])
        return True, data
    error = HttpClient.safe_json_get(response, "error", error_message)
    return False, error

def handle_search_response(response, error_message):
    if response.ok:
        data = HttpClient.safe_extract_data(response, [])
        return True, data
    return False, error_message
