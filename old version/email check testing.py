import re

def is_valid_email(email):
    # Regular expression pattern for a valid email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(email_pattern, email))

# Test cases
print(is_valid_email("test@example.com"))    # ✅ True (Valid)
print(is_valid_email("user123@gmail.com"))   # ✅ True (Valid)
print(is_valid_email("user.name@domain.co")) # ✅ True (Valid)
print(is_valid_email("user@sub.domain.com")) # ✅ True (Valid)

# Invalid cases
print(is_valid_email("user@domain"))         # ❌ False (No top-level domain)
print(is_valid_email("user@@domain.com"))    # ❌ False (Double @)
print(is_valid_email("user.com"))            # ❌ False (Missing @)
print(is_valid_email("user@domain..com"))    # ❌ False (Double dot)
print(is_valid_email("user@domain.c"))       # ❌ False (TLD too short)
