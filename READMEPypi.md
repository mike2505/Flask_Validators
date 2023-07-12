# Flask Validator

Flask Validator is a powerful package designed to simplify data validation in Flask applications. It provides an easy-to-use interface for defining data validation rules and seamlessly integrates with Flask routes using a custom decorator.

* **Simplified Data Validation:** Flask Validator streamlines the process of validating data in Flask applications, reducing the complexity and boilerplate code.
* **Integration with Flask Routes:** The package seamlessly integrates with Flask routes through a custom decorator, making it easy to apply validation rules to specific endpoints.
* **Flexible Validation Schema:** Flask Validator allows you to define validation rules using a schema structure, providing a clear and organized way to specify the expected data format.
* **Custom Validators:** You can create custom validators to extend the validation capabilities of Flask Validator, enabling you to implement complex validation logic tailored to your application's needs.
* **Error Handling:** Flask Validator automatically generates error messages based on the defined validation rules, simplifying the process of handling validation failures and providing 

With the help of Flask Validator, you can ensure the integrity and consistency of the data submitted to your Flask endpoints, enhancing the reliability and security of your application.

## How It Works

1. Flask Validator provides a custom decorator, @validate_form, which can be applied to Flask routes.
2. The decorator takes a validation schema as its argument, defined using the Schema class and Field class from Flask Validator. 
3. The validation schema specifies the structure of the expected data and the validation rules for each field.
4. When a request is made to a decorated route, Flask Validator automatically validates the incoming data based on the defined schema.
5. If the data passes the validation, the route handler function is executed as usual.
6. If the data fails the validation, Flask Validator generates error messages based on the defined rules and returns a response with the error details.

## Usage
To use Flask Validator in your Flask application, follow these steps:

### Installation
You can install Flask Validator using pip:

```
pip install flask_validators
```

### Getting Started
1. Import the necessary modules and classes from Flask Validator:
```python
from flask import Flask, request, jsonify
from flask_validators import validate_form
```

2. Create a Flask application instance:
```python
app = Flask(__name__)
```

3. Define a route with the @validate_form decorator and specify the validation schema:
```python
@app.route('/validate', methods=['POST'])
@validate_form('age', 'name', 'email')
def validate_data():
    return jsonify({'success': True, 'message': 'Data is valid.'})
```

4. Run the Flask application:
```python
if __name__ == '__main__':
    app.run(debug=True)
```

Now, when a POST request is made to the /validate endpoint, Flask Validator will automatically validate the incoming data based on the specified schema. The @validate_form decorator is used to validate the fields 'age', 'name', and 'email'. If the data passes the validation, the route handler function (validate_data in this case) will be executed. Otherwise, Flask Validator will generate error messages and return a response with the error details.

You can also define Validators with specific requirements
```python
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
```

## Validation Schema
The validation schema is defined using the Schema class, which takes a dictionary representing the schema structure. Each field in the schema is associated with a set of validation rules.
For example, the following schema validates an email field:
```python
Schema({
    'email': Field(required=True, type='string', validators=[
        {'name': 'email', 'message': 'Invalid email address.'}
    ])
})
```
In the example above, the email field is marked as required and expects a string value. It also applies an additional validator to check if the value is a valid email address.

## Database validation
Flask Validator provides database validation capabilities through the validate_db decorator. This allows you to validate data based on database constraints and perform various checks against the database.

To use database validation, you need to have SQLAlchemy set up in your Flask application. Flask Validator integrates with SQLAlchemy to perform database-related validations.

Here are some examples of database validations:

### Unique check
```python
@app.route('/check_unique', methods=['POST'])
@validate_db(User, Session, email=['check_unique'])
def check_unique_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})
```

```bash
curl -X POST \
  -d "email=test@example.com" \
  http://localhost:5000/check_unique
```

Response:
```bash
{
  "email": "Email already exists."
}
```

This example validates the email field against uniqueness constraints in the User table using the check_unique validator.

### Null check
```python
@app.route('/check_null', methods=['POST'])
@validate_db(User, Session, username=['check_null'])
def check_null_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})
```
This example validates the username field against null constraints in the User table using the check_null validator.

### Check Existence
```python
@app.route('/check_existence', methods=['POST'])
@validate_db(User, Session, id=['check_existence'])
def check_existence_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})
```
This example validates the id field by checking its existence in the User table using the check_existence validator.

### Check Range
```python
@app.route('/check_range', methods=['POST'])
@validate_db(User, Session, username=['check_range'])
def check_range_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})
```
This example validates the username field against a range constraint in the User table using the check_range validator.

### Check Type
```python
@app.route('/check_type', methods=['POST'])
@validate_db(User, Session, username=['check_type'])
def check_type_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})
```
This example validates the username field against a specific data type constraint in the User table using the check_type validator.

### Check Enum
```python
@app.route('/check_enum', methods=['POST'])
@validate_db(User, Session, status=['check_enum'])
def check_enum_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})
```
This example validates the status field against an enumeration constraint in the User table using the check_enum validator.

### Check Length
```python
@app.route('/check_length', methods=['POST'])
@validate_db(User, Session, username=['check_length'])
def check_length_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})
```
This example validates the username field against a length constraint in the User table using the check_length validator.

## LLM Validators 
Flask Validator also provides language validation capabilities through the validate_llm decorator. This allows you to validate text against specific languages using Language Models (LLMs).

To use language validation, you need to have access to a suitable language model. Flask Validator integrates with LLMs to perform language-related validations.

Here is an example of language validation:
```python
@app.route('/validate_language', methods=['POST'])
@validate_llm(text=['validate_language'], lang='ka')
def validate_lang():
    return jsonify({'success': True, 'message': 'Data is valid.'})
```
In this example, the @validate_llm decorator is applied to the /validate_language route. The text field is specified for language validation, and the lang parameter is set to 'ka', which represents the Georgian language.

When a POST request is made to this endpoint, Flask Validator will use the specified LLM for the Georgian language to validate the input text. If the text is determined to be valid according to the language model, the route handler function will be executed, and a response indicating the success of the validation will be returned.

Language validation can be beneficial in various scenarios. For example, you can use it to validate user-generated content, ensure that text inputs are written in the correct language for multilingual applications, or filter out content that violates language-specific guidelines or restrictions.

supported languages:

```af, am, an, ar, as, az, be, bg, bn, br, bs, ca, cs, cy, da, de, dz, el, en, eo, es, et, eu, fa, fi, fo, fr, ga, gl, gu, he, hi, hr, ht, hu, hy, id, is, it, ja, jv, ka, kk, km, kn, ko, ku, ky, la, lb, lo, lt, lv, mg, mk, ml, mn, mr, ms, mt, nb, ne, nl, nn, no, oc, or, pa, pl, ps, pt, qu, ro, ru, rw, se, si, sk, sl, sq, sr, sv, sw, ta, te, th, tl, tr, ug, uk, ur, vi, vo, wa, xh, zh, zu```

## Validation Rules
Validation rules are defined using the Field class. Each field can have properties such as required (indicating if the field is required), type (specifying the expected data type), and validators (a list of additional validators to apply).

The Field class also provides built-in validation methods, such as validate_email, validate_age, validate_name, validate_password, and validate_json. These methods can be used directly or extended to implement custom validation logic.

## Custom Validators
Flask Validator allows you to create custom validators to implement complex validation logic tailored to your application's needs. To create a custom validator, define a method within the Schema class that follows the validate_<validator_name> naming convention. This method should accept the field value and any additional arguments defined in the validation rule. It should return a tuple with a boolean indicating the validation result and an error message if the validation fails.

For example, to create a custom validator named validate_custom, add the following method to the Schema class:
```python
def validate_custom(self, value, argument1, argument2, ...):
    # Validation logic
    if valid:
        return True, None
    else:
        return False, 'Validation failed.'
```

## Error Handling
If validation fails, Flask Validator automatically generates error messages based on the defined validation rules. The error response includes a JSON object with the field names as keys and the corresponding error messages as values. This makes it easier to handle validation failures and provide meaningful feedback to the users.