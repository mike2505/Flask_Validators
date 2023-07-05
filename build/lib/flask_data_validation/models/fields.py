import re
import json

from urllib.parse import urlparse
from datetime import datetime

class Field:
    def __init__(self, required=False, type=None, validators=None):
        self.required = required
        self.type = type
        self.validators = validators or []

    def validate(self, value):
        if self.required and value is None:
            return False, 'This field is required.'

        if self.type:
            if self.type == 'string' and not isinstance(value, str):
                return False, 'Expected a string.'
            elif self.type == 'integer' and not isinstance(value, int):
                return False, 'Expected an integer.'
            elif self.type == 'float' and not isinstance(value, float):
                return False, 'Expected a float.'
            elif self.type == 'boolean' and not isinstance(value, bool):
                return False, 'Expected a boolean.'
            # Add more type validations as needed

        for validator in self.validators:
            validator_name = validator['name']
            if validator_name == 'min_age':
                validator_name = 'age'
            elif validator_name == 'max_age':
                validator_name = 'age'
            elif validator_name == 'email':
                validator_name = 'email'

            validator_func = getattr(self, f'validate_{validator_name}', None)
            if not validator_func:
                continue

            validator_args = validator.get('args', ())
            validator_kwargs = validator.get('kwargs', {})

            if validator_name == 'age':
                min_age, max_age = validator_args
                is_valid, error_message = validator_func(value, min_age, max_age, **validator_kwargs)
            else:
                is_valid, error_message = validator_func(value, *validator_args, **validator_kwargs)

            if not is_valid:
                return False, error_message

        return True, None

    def validate_email(self, value):
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            return True, None
        return False, 'Invalid email address.'

    def validate_name(self, value):
        if isinstance(value, str) and value.strip():
            return True, None
        return False, 'Invalid name.'

    def validate_age(self, value, min_age=0, max_age=120):
        if isinstance(value, int) and min_age <= value <= max_age:
            return True, None
        return False, f'Age must be between {min_age} and {max_age}.'

    def validate_password(self, value, min_length=8, max_length=16, require_special_char=True):
        if isinstance(value, str) and min_length <= len(value) <= max_length:
            if require_special_char and re.search(r'\W', value):
                return True, None
        return False, 'Invalid password.'

    def validate_json(self, value):
        try:
            json.loads(value)
            return True, None
        except json.JSONDecodeError:
            return False, 'Invalid JSON.'

    def validate_phone(self, value):
        if re.match(r'^\+?1?\d{9,15}$', value):
            return True, None
        return False, 'Invalid phone number.'

    def validate_zipcode(self, value):
        if re.match(r'^\d{5}(-\d{4})?$', value):  # US zipcode format
            return True, None
        return False, 'Invalid zipcode.'

    def validate_date(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')  # assuming date format to be 'YYYY-MM-DD'
            return True, None
        except ValueError:
            return False, 'Invalid date.'

    def validate_credit_card(self, value):
        # naive check for 16 digit number with optional hyphens or spaces
        if re.match(r'^(\d{4}[-\s]?){3}\d{4}$', value):
            return True, None
        return False, 'Invalid credit card number.'

    def validate_ssn(self, value):
        # naive check for US SSN (XXX-XX-XXXX)
        if re.match(r'^\d{3}-\d{2}-\d{4}$', value):
            return True, None
        return False, 'Invalid social security number.'

    def validate_url(self, value):
        try:
            result = urlparse(value)
            return all([result.scheme, result.netloc]), 'Invalid URL.'
        except ValueError:
            return False, 'Invalid URL.'

    def validate_ip_address(self, value):
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', value):  # naive IPv4 check
            return True, None
        return False, 'Invalid IP address.'

    def validate_hex_color(self, value):
        if re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value):
            return True, None
        return False, 'Invalid hexadecimal color code.'

    def validate_latitude(self, value):
        if re.match(r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$', value):
            return True, None
        return False, 'Invalid latitude.'

    def validate_longitude(self, value):
        if re.match(r'^[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$', value):
            return True, None
        return False, 'Invalid longitude.'