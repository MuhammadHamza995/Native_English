# shared/validators.py

from rest_framework.exceptions import ValidationError

def validate_password(value):
    """Ensure the password is at least 8 characters long."""
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    return value

def validate_username(value):
    """Ensure the username is at least 3 characters long."""
    if len(value) < 3:
        raise ValidationError("Username must be at least 3 characters long")
    return value

def validate_role(value):
    """Ensure the role is either 'admin' or 'user'."""
    if value not in ['admin', 'user']:
        raise ValidationError("Role must be either 'admin' or 'user'")
    return value
