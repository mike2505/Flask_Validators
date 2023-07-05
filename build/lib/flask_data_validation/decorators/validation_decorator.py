from functools import wraps
from flask import request, jsonify
from flask_data_validation.controllers.validator import DataValidator
from flask_data_validation.models.schema import Schema
from flask_data_validation.models.fields import Field

field_schemas = {
    'email': Field(required=True, type='string', validators=[
        {'name': 'email', 'message': 'Invalid email address.'}
    ]),
    'name': Field(required=True, type='string', validators=[
        {'name': 'name', 'message': 'Invalid name.'}
    ]),
    'age': Field(required=True, type='integer', validators=[
        {'name': 'age', 'message': 'Invalid age.', 'args': (0, 120)}
    ]),
    'password': Field(required=True, type='string', validators=[
        {'name': 'password', 'message': 'Invalid password.', 'kwargs': {'min_length': 8, 'max_length': 16, 'require_special_char': True}}
    ]),
    'json': Field(required=True, type='string', validators=[
        {'name': 'json', 'message': 'Invalid JSON.'}
    ]),
    'phone': Field(required=True, type='string', validators=[
        {'name': 'phone', 'message': 'Invalid phone number.'}
    ]),
    'zipcode': Field(required=True, type='string', validators=[
        {'name': 'zipcode', 'message': 'Invalid zipcode.'}
    ]),
    'date': Field(required=True, type='string', validators=[
        {'name': 'date', 'message': 'Invalid date.'}
    ]),
    'credit_card': Field(required=True, type='string', validators=[
        {'name': 'credit_card', 'message': 'Invalid credit card number.'}
    ]),
    'ssn': Field(required=True, type='string', validators=[
        {'name': 'ssn', 'message': 'Invalid social security number.'}
    ]),
    'url': Field(required=True, type='string', validators=[
        {'name': 'url', 'message': 'Invalid URL.'}
    ]),
    'ip_address': Field(required=True, type='string', validators=[
        {'name': 'ip_address', 'message': 'Invalid IP address.'}
    ]),
    'hex_color': Field(required=True, type='string', validators=[
        {'name': 'hex_color', 'message': 'Invalid hexadecimal color code.'}
    ]),
    'latitude': Field(required=True, type='string', validators=[
        {'name': 'latitude', 'message': 'Invalid latitude.'}
    ]),
    'longitude': Field(required=True, type='string', validators=[
        {'name': 'longitude', 'message': 'Invalid longitude.'}
    ]),
}

def validate_form(*fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()

            if not data:
                return jsonify({'error': 'No data provided.'}), 400

            errors = {}
            for field in fields:
                if field not in field_schemas:
                    continue

                schema = field_schemas[field]

                if field not in data:
                    errors[field] = "Missing data"
                    continue

                value = data.get(field)

                is_valid, error_message = schema.validate(value)
                if not is_valid:
                    errors[field] = error_message

            if errors:
                return jsonify(errors), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator