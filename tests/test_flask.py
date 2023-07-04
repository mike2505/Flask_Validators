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