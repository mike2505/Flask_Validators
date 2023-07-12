from functools import wraps
from flask import request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import String, Integer
import re

def check_unique(model_class, session, value, data):
    query = session.query(model_class).filter(getattr(model_class, data.get('field')) == value).first()
    if query and query.id != data.get('id'):  # Compare against the existing record's ID
        return False, f'{data.get("field").capitalize()} already exists.'
    return True, None

def check_null(model_class, session, value, data):
    if not value:
        return False, f'{data.get("field").capitalize()} is required.'
    return True, None

def check_existence(model_class, session, value, data):
    id_value = value
    if id_value:
        query = session.query(model_class).filter(getattr(model_class, data.get('field')) == id_value).first()
        if not query:
            return False, f'{data.get("field").capitalize()} does not exist.'
    return True, None

def check_range(model_class, session, value, data):
    field_range = data.get('range', (0, 100))  # Default range if not provided
    if len(value) < field_range[0] or len(value) > field_range[1]:
        return False, f'{data.get("field").capitalize()} must be between {field_range[0]} and {field_range[1]} characters.'
    return True, None

def check_type(model_class, session, value, data):
    if value is None:  # Do not perform type checking on None values
        return True, None
    expected_type = python_type(getattr(model_class, data.get('field')).type)
    if not isinstance(value, expected_type):
        return False, f'{data.get("field").capitalize()} must be of type {expected_type.__name__}.'
    return True, None

def python_type(sqla_type):
    if isinstance(sqla_type, String):
        return str
    elif isinstance(sqla_type, Integer):
        return int
    # Add more type conversions if needed
    else:
        return type(None)  # If unknown, return NoneType

def check_enum(model_class, session, value, data):
    # Assumes data['enum'] is a list of valid options
    if value not in data.get('enum', []):
        return False, f'{data.get("field").capitalize()} is not a valid option.'
    return True, None

def check_length(model_class, session, value, data):
    # Checks if the length of the value is not beyond the specified limit
    limit = data.get('length')
    if limit and len(value) > limit:
        return False, f'{data.get("field").capitalize()} exceeds the length limit.'
    return True, None