class DataValidator:
    def __init__(self, schema, data):
        self.schema = schema
        self.data = data

    def validate(self):
        errors = {}
        for field_name, field in self.schema.fields.items():
            value = self.data.get(field_name)
            if value is None and field.required:
                errors[field_name] = 'This field is required.'
            elif value is not None:
                is_valid, error_message = field.validate(value)
                if not is_valid:
                    errors[field_name] = error_message
        return errors