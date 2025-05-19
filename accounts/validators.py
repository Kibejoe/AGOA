import re
from django.core.exceptions import ValidationError

class StrongPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError("The password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("The password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("The password must contain at least one digit.")
        if not re.search(r'[\W_]', password):  # \W is non-alphanumeric
            raise ValidationError("The password must contain at least one special character.")

    def get_help_text(self):
        return "Your password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
