# Flask_Validator
Flask_Validator is a powerful package designed to simplify data validation in Flask applications. It provides an easy-to-use interface for defining data validation rules and seamlessly integrates with Flask routes using a custom decorator.

### Installation
You can install Flask_Validator using pip:
```
pip install Flask_Validator
```
### Getting Started
To use Flask_Validator in your Flask application, follow these steps:

```
from flask import Flask, request, jsonify
from flask_data_validation.decorators.validation_decorator import validate_form
from flask_data_validation.models.schema import Schema
from flask_data_validation.models.fields import Field

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
@validate_form(
    Schema({
        'email': Field(required=True, type='string', validators=[
            {'name': 'email', 'message': 'Invalid email address.'}
        ])
    })
)
def validate_data():
    return jsonify({'success': True, 'message': 'Data is valid.'})

if __name__ == '__main__':
    app.run(debug=True)
```
    
### Validation Schema
The validation schema is defined using the Schema class, which takes a dictionary representing the schema structure. Each field in the schema is associated with a set of validation rules.

For example, the following schema validates an email field:

```
Schema({
    'email': Field(required=True, type='string', validators=[
        {'name': 'email', 'message': 'Invalid email address.'}
    ])
})
```
In the example above, the email field is marked as required and expects a string value. It also applies an additional validator to check if the value is a valid email address.

### Validation Rules
Validation rules are defined using the Field class. Each field can have the following properties:

required: Indicates if the field is required.
type: Specifies the expected data type of the field (e.g., 'string', 'integer', 'float', 'boolean').
validators: A list of additional validators to apply to the field.
The Field class also provides several built-in validation methods, such as validate_email, validate_age, validate_name, validate_password, and validate_json. You can extend these methods or create your own custom validators.

### Custom Validators
To create a custom validator, define a method within the Schema class that follows the validate_<validator_name> naming convention. This method should accept the field value and any additional arguments defined in the validation rule. It should return a tuple of boolean and error message.

For example, to create a custom validator named validate_custom, add the following method to the Schema class:

```
def validate_custom(self, value, argument1, argument2, ...):
    # Validation logic
    if valid:
        return True, None
    else:
        return False, 'Validation failed.'
```
### Error Handling
If validation fails, Flask_Validator automatically generates error messages based on the defined validation rules. The error response includes a JSON object with the field names as keys and the corresponding error messages as values.

### Conclusion
Flask_Validator simplifies the process of data validation in Flask applications. It provides a flexible and intuitive way to define validation rules and seamlessly integrate them into your routes. By using Flask_Validator, you can ensure the integrity and consistency of the data submitted to your Flask endpoints.
