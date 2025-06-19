from flask import jsonify
from http import HTTPStatus

def success_response(data=None, message="Success", status=HTTPStatus.OK):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status

def error_response(message="Something went wrong", status=HTTPStatus.BAD_REQUEST):
    return jsonify({
        "success": False,
        "message": message
    }), status
