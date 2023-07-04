from functools import wraps
from flask import request, jsonify
from flask_data_validation.controllers.validator import DataValidator

def validate_form(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            errors = DataValidator(schema, data).validate()  # Updated line
            if errors:
                return jsonify(errors), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator