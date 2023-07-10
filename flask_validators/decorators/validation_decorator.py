from functools import wraps
from flask import request, jsonify
from flask_validators.controllers.validator import DataValidator
from flask_validators.models.schema import Schema
from flask_validators.models.fields import Field
from flask_validators.models.validate_db import check_unique_fields
from sqlalchemy.orm import sessionmaker

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
    'confirm_password': Field(required=True, type='string', validators=[
        {'name': 'confirm_password', 'message': 'Passwords must match.', 'kwargs': {'password_field': 'password'}}
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
    'file': Field(required=True, type='file', validators=[
        {'name': 'file', 'message': 'Invalid file.', 'kwargs': {'allowed_extensions': ['jpg', 'png', 'pdf', 'txt'], 'max_size': 1024 * 1024 * 5}}  # 5MB
    ]),
}

def validate_form(*fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.form.to_dict()
            file_data = {k: v for k, v in request.files.items() if k in fields}

            if not data and not file_data:
                return jsonify({'error': 'No data provided.'}), 400

            errors = {}
            for field in fields:
                if field not in field_schemas:
                    continue

                schema = field_schemas[field]
                schema.data = data  # Pass the whole data
                value = data.get(field) if field in data else file_data.get(field)

                if not value:
                    errors[field] = "Missing data"
                    continue

                is_valid, error_message = schema.validate(value)
                if not is_valid:
                    errors[field] = error_message

            if errors:
                return jsonify(errors), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_db(model_class, Session, unique_fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            session = Session()

            data = request.form.to_dict()
            errors = {}

            # Check unique fields
            errors.update(check_unique_fields(model_class, unique_fields, session, data))

            if errors:
                return jsonify(errors), 400

            return f(*args, **kwargs)

        return decorated_function

    return decorator
