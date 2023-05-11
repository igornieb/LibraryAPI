from django.core.exceptions import ValidationError
import re
def ISBNValidator(isbn):
    isbn = isbn.replace("-", "").replace(" ", "").upper();
    match = re.search(r'^(\d{9})(\d|X)$', isbn)
    if not match:
        raise ValidationError("incorect isbn")

    digits = match.group(1)
    check_digit = 10 if match.group(2) == 'X' else int(match.group(2))

    result = sum((i + 1) * int(digit) for i, digit in enumerate(digits))
    if (result % 11) == check_digit:
        return isbn
    raise ValidationError("incorect isbn")