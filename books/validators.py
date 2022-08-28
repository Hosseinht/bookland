from django.core.validators import RegexValidator


def validate_isbn():
    validator = RegexValidator(r'^[0-9]*$', 'ISBN contains numbers not words!')
    return validator
