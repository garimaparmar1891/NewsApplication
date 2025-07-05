from flask import jsonify

def success_response(data=None, message=None, status=200):
    response = {}
    if message:
        response["message"] = message
    if data is not None:
        response["data"] = data
    return jsonify(response), status

def error_response(message, status):
    return jsonify({"error": message}), status
