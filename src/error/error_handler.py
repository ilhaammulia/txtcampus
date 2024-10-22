from flask import jsonify

def handle_not_found(error):
    response = jsonify({"success": False, "message": error.message, "data": None})
    response.status_code = error.status_code
    return response

def handle_internal_error(error):
    response = jsonify({"success": False, "message": error.message, "data": None})
    response.status_code = error.status_code
    return response

def handle_bad_request(error):
    response = jsonify({"success": False, "message": error.message, "data": None})
    response.status_code = error.status_code
    return response

def handle_forbidden_error(error):
    response = jsonify({"success": False, "message": error.message, "data": None})
    response.status_code = error.status_code
    return response

def handle_unauthorized_error(error):
    response = jsonify({"success": False, "message": error.message, "data": None})
    response.status_code = error.status_code
    return response
