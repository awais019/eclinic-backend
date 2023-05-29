from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size = 2 * 1024 * 1024

    if file.size > max_size:
        raise ValidationError(f'File size should not exceed {max_size} bytes')