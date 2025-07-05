from flask_jwt_extended import get_jwt_identity
from utils.response_utils import error_response
from constants import messages
from http import HTTPStatus
from flask import request
from typing import Optional, Tuple, Any


class BaseController:
    
    def _get_user_id(self):
        return get_jwt_identity()
    
    def _validate_required_dates(self, start_date, end_date):
        if not start_date or not end_date:
            return error_response(messages.MISSING_REQUIRED_FIELDS, HTTPStatus.BAD_REQUEST)
        return None
    
    def _get_date_range_params(self):
        return (
            request.args.get("start_date"),
            request.args.get("end_date")
        )
    
    def _get_validated_date_params(self):
        start_date, end_date = self._get_date_range_params()
        validation_error = self._validate_required_dates(start_date, end_date)
        if validation_error:
            return validation_error
        return {'start_date': start_date, 'end_date': end_date}
    
    def _get_request_param(self, param_name, required=False):
        value = request.args.get(param_name)
        if required and not value:
            return error_response(messages.MISSING_REQUIRED_FIELDS, HTTPStatus.BAD_REQUEST)
        return value
    
    def _validate_json_data(self, required_fields: Optional[list] = None, missing_fields_message: Optional[str] = None) -> Tuple[Optional[dict], Optional[Any]]:
        data = request.get_json()
        if not data:
            message = missing_fields_message if missing_fields_message is not None else messages.MISSING_REQUIRED_FIELDS
            return None, error_response(message, HTTPStatus.BAD_REQUEST)
        if required_fields:
            for field in required_fields:
                if not data.get(field):
                    return None, error_response(f"{field} is required", HTTPStatus.BAD_REQUEST)
        return data, None 
