import logging
import traceback
from functools import wraps
from flask import jsonify, has_request_context
from utils.custom_exceptions import AppError

DEFAULT_ERROR_MESSAGE = "Unexpected server error"
DEFAULT_STATUS_CODE = 500

logger = logging.getLogger(__name__)


def _create_error_response(error_message, status_code):
    return {"error": error_message, "status_code": status_code}


def _format_flask_response(error_message, status_code):
    return jsonify({"error": error_message}), status_code


def _log_exception(exception, context="Unknown"):
    logger.error(
        "Exception in %s: %s\nTraceback:\n%s",
        context,
        str(exception),
        traceback.format_exc()
    )


def handle_exceptions():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except AppError as app_error:
                if has_request_context():
                    return _format_flask_response(app_error.message, app_error.status_code)
                return _create_error_response(app_error.message, app_error.status_code)
            except Exception as exception:
                _log_exception(exception, func.__name__)
                
                if has_request_context():
                    return _format_flask_response(DEFAULT_ERROR_MESSAGE, DEFAULT_STATUS_CODE)
                return _create_error_response(DEFAULT_ERROR_MESSAGE, DEFAULT_STATUS_CODE)
        return wrapper
    return decorator
