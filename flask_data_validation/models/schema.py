import re
import json

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