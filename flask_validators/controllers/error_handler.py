from flask import jsonify

class ErrorHandler:
    @staticmethod
    def handle_validation_error(error):
        response = jsonify({"errors": error.args[0]})
        response.status_code = 400
        return response