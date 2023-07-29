from marshmallow.exceptions import ValidationError

# Create function to validate any names
def validate_name(value, field):
    if value.startswith('-') or value.startswith(' '):
        raise ValidationError(f'{field} must start with a letter. It cannot start with a hyphen (\'-\') or space (\' \').')
    
    if value.endswith('-') or value.endswith(' '):
        raise ValidationError(f'{field} must end with a letter. It cannot end with a hyphen (\'-\') or space (\' \').')
    
    return value


# Create function to validate phone numbers
def validate_number(value, field):
    if len(value) < 8:
        raise ValidationError(f'{field} must be at least 8 characters long.')
    
    if value.startswith(' '):
        raise ValidationError(f'{field} must start with a number. It cannot start with a space (\' \').')
    
    if value.endswith(' '):
        raise ValidationError(f'{field} must end with a number. It cannot end with a space (\' \').')
    
    return value