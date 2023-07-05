from flask import Flask, request, jsonify
from flask_validators import validate_form, Schema, Field, DataValidator

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

@app.route('/validate2', methods=['POST'])
@validate_form('age', 'name', 'email')
def validate_data2():
    return jsonify({'success': True, 'message': 'Data is valid.'})

if __name__ == '__main__':
    app.run(debug=True) 