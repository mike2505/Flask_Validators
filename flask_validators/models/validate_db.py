from functools import wraps
from flask import request, jsonify
from sqlalchemy.orm import sessionmaker

def check_unique_fields(model_class, unique_fields, session, data):
    errors = {}
    for field in unique_fields:
        value = data.get(field)
        if value:
            query = session.query(model_class).filter(getattr(model_class, field) == value).first()
            if query and query.id != data.get('id'):  # Compare against the existing record's ID
                errors[field] = f'{field.capitalize()} already exists.'

    return errors