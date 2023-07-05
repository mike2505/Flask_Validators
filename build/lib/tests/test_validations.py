import unittest
from flask_data_validation.controllers.validator import DataValidator
from flask_data_validation.models.schema import Schema
from flask_data_validation.models.fields import Field

class TestDataValidation(unittest.TestCase):
    def test_valid_data(self):
        # Define the validation schema
        schema = Schema({
            'name': Field(required=True, type='string'),
            'age': Field(required=True, type='integer', validators=[
                {'name': 'age', 'args': (18, 65), 'message': 'Age must be between 18 and 65.'},
            ]),
            'email': Field(required=True, type='string', validators=[
                {'name': 'email', 'message': 'Invalid email address.'}
            ])
        })

        # Create the data validator
        data = {
            'name': 'John Doe',
            'age': 19,
            'email': 'johndoe@example.com'
        }
        validator = DataValidator(schema, data)

        # Test valid data
        errors = validator.validate()
        self.assertEqual(errors, {})  # No errors should be returned for valid data

    def test_invalid_name(self):
        # Define the validation schema
        schema = Schema({
            'name': Field(required=True, type='string', validators=[
                 {'name': 'name', 'message': 'Invalid name.'}
            ]),
            'age': Field(required=True, type='integer', validators=[
                {'name': 'age', 'args': (18, 65), 'message': 'Age must be between 18 and 65.'},
            ]),
            'email': Field(required=True, type='string', validators=[
                {'name': 'email', 'message': 'Invalid email address.'}
            ])
        })

        # Create the data validator
        data = {
            'name': '',
            'age': 18,
            'email': 'johndoe@example.com'
        }
        validator = DataValidator(schema, data)

        # Test invalid name
        errors = validator.validate()
        expected_errors = {'name': 'Invalid name.'}
        self.assertEqual(errors, expected_errors)

    def test_invalid_password(self):
        schema = Schema({
            'password': Field(required=True, type='string', validators=[
                {
                    'name': 'password',
                    'args': (8, 16, True),  # Here False means we do not require special characters
                    'message': 'Invalid password.'
                }
            ])
        })

        data = {
            'name': '',
            'age': 18,
            'email': 'johndoe@example.com',
            'password': '12345678'
        }
        validator = DataValidator(schema, data)

        # Test invalid name
        errors = validator.validate()
        expected_errors = {'password': 'Password must contain at least one special character.'}
        self.assertEqual(errors, expected_errors)

    def test_invalid_json(self):
        schema = Schema({
            'data': Field(required=True, type='string', validators=[
                {
                    'name': 'json',
                    'message': 'Invalid JSON data.'
                }
            ])
        })

        data = {
            'data': 'asdad'
        }
        validator = DataValidator(schema, data)

        # Test invalid name
        errors = validator.validate()
        expected_errors = {'data': 'Invalid JSON.'}
        self.assertEqual(errors, expected_errors)

if __name__ == '__main__':
    unittest.main()