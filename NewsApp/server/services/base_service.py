from flask import jsonify
from utils.custom_exceptions import AppError
from http import HTTPStatus

class BaseService:
    
    @staticmethod
    def success_response(data=None, message=None, status=200):
        response = {}
        if message:
            response["message"] = message
        if data is not None:
            response["data"] = data
        return jsonify(response), status
    
    def _create_success_response(self, data=None, message=None):
        return self.success_response(data=data, message=message)
    
    def _validate_required_fields(self, *fields, error_message="Missing required fields"):
        if not all(fields):
            raise AppError(error_message, HTTPStatus.BAD_REQUEST)
    
    def _handle_empty_result(self, result, error_message, status_code=HTTPStatus.NOT_FOUND):
        if not result:
            raise AppError(error_message, status_code)
        return result
