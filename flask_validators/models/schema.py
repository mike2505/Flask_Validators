import re
import json

from urllib.parse import urlparse
from datetime import datetime

class Schema:
    def __init__(self, schema):
        self.schema = schema
        self.fields = schema

    def validate(self, data):
        errors = {}
        for field, rules in self.schema.items():
            value = data.get(field)
            field_errors = []

            if rules.get('required') and not value:
                field_errors.append('This field is required.')

            if 'type' in rules and not self.validate_type(value, rules['type']):
                field_errors.append(f'Expected a {rules["type"]}.')

            if 'validators' in rules:
                for validator in rules['validators']:
                    validator_name = validator['name']
                    validator_func = getattr(self, f'validate_{validator_name}')
                    validator_args = validator.get('args', ())
                    validator_kwargs = validator.get('kwargs', {})

                    if not validator_func(value, *validator_args, **validator_kwargs):
                        field_errors.append(validator['message'])

            if field_errors:
                errors[field] = field_errors[0] if len(field_errors) == 1 else field_errors

        return errors

    def validate_type(self, value, expected_type):
        if expected_type == 'string':
            return isinstance(value, str)
        elif expected_type == 'integer':
            return isinstance(value, int)
        elif expected_type == 'float':
            return isinstance(value, float)
        elif expected_type == 'boolean':
            return isinstance(value, bool)
        # Add more type validations as needed

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

    def validate_file(self, value, allowed_extensions=None, max_size=None):
        if allowed_extensions and value.filename.split('.')[-1] not in allowed_extensions:
            return False, 'Invalid file extension.'
        
        if max_size and value.content_length > max_size:
            return False, 'File size is too large.'

        return True, None

    def validate_confirm_password(self, value, password_field):
        password = self.data.get(password_field)
        if password != value:
            return False, 'Passwords must match.'
        return True, None