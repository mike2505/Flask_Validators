import re
import json

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
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            return False, 'Invalid email address.'
        return True, None

    def validate_age(self, value, min_age, max_age):
        if not isinstance(value, int):
            return False, 'Age must be an integer.'

        if value < min_age:
            return False, f'Age must be at least {min_age}.'

        if value > max_age:
            return False, f'Age must be at most {max_age}.'

        return True, None

    def validate_name(self, value):
        if isinstance(value, str) and value.strip():
            return True, None

        return False, 'Invalid name.'

    def validate_password(self, value, min_length=8, max_length=16, require_special_char=True):
        if not isinstance(value, str):
            return False, 'Password must be a string.'

        if not min_length <= len(value) <= max_length:
            return False, f'Password must be between {min_length} and {max_length} characters long.'

        if require_special_char and not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            return False, 'Password must contain at least one special character.'

        return True, None

    def validate_json(self, value):
        if not isinstance(value, str):
            return False, 'JSON input must be a string.'

        try:
            json.loads(value)
        except json.JSONDecodeError:
            return False, 'Invalid JSON.'

        return True, None