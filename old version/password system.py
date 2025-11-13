import re

def is_valid_password(password, min_length=8):
    # Check for minimum length
    if len(password) < min_length:
        return False

    # Check for at least one uppercase letter, one number, and one special character
    has_uppercase = re.search(r'[A-Z]', password)
    has_number = re.search(r'\d', password)  # \d matches any digit (0-9)
    has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)  # Adjust for allowed special chars

    return bool(has_uppercase and has_number and has_special)

# Test cases
print(is_valid_password("Hello123!", 8))  # True (Valid)
print(is_valid_password("hello123!", 8))  # False (No uppercase letter)
print(is_valid_password("HELLO123", 8))   # False (No special character)
print(is_valid_password("H1!", 8))        # False (Too short)
print(is_valid_password("Hello@World123", 8))  # True (Valid)
