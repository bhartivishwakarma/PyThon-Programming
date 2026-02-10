"""
CONCEPT: Advanced Pattern Validation
Combine regex concepts for real-world validation

Common Validations:
- Email addresses
- Phone numbers
- URLs
- IP addresses
- Dates
- Passwords

Validation Strategy:
1. Define pattern with anchors (^ $)
2. Use appropriate character classes
3. Add quantifiers for repetition
4. Test with valid and invalid examples
"""

import re

print("="*70)
print("Program 7: ADVANCED VALIDATION")
print("="*70)

# Example 1: Email validation
def validate_email(email):
    """
    Validate email address
    Pattern: username@domain.tld
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.fullmatch(pattern, email) is not None

emails = [
    "user@example.com",      # Valid
    "user.name@test.co.uk",  # Valid
    "user+tag@domain.org",   # Valid
    "invalid.email",         # Invalid - no @
    "@nodomain.com",         # Invalid - no username
    "user@.com"              # Invalid - no domain
]

print("\n1. EMAIL VALIDATION:")
for email in emails:
    result = "✓ Valid" if validate_email(email) else "✗ Invalid"
    print(f"   {result}: {email}")

# Example 2: Phone number validation
def validate_phone(phone):
    """
    Validate phone number
    Formats: (123) 456-7890, 123-456-7890, 123.456.7890
    """
    pattern = r'^(\(\d{3}\)\s*|\d{3}[-.]?)\d{3}[-.]?\d{4}$'
    return re.fullmatch(pattern, phone) is not None

phones = [
    "(123) 456-7890",  # Valid
    "123-456-7890",    # Valid
    "123.456.7890",    # Valid
    "1234567890",      # Valid
    "12-345-6789",     # Invalid - wrong format
    "123-45-6789"      # Invalid - too few digits
]

print("\n2. PHONE NUMBER VALIDATION:")
for phone in phones:
    result = "✓ Valid" if validate_phone(phone) else "✗ Invalid"
    print(f"   {result}: {phone}")

# Example 3: URL validation
def validate_url(url):
    """
    Validate URL
    Pattern: protocol://domain.tld/path
    """
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
    return re.fullmatch(pattern, url) is not None

urls = [
    "http://example.com",           # Valid
    "https://www.test.org/path",    # Valid
    "https://sub.domain.co.uk",     # Valid
    "ftp://files.com",              # Invalid - wrong protocol
    "http://invalid",               # Invalid - no TLD
    "www.missing-protocol.com"      # Invalid - no protocol
]

print("\n3. URL VALIDATION:")
for url in urls:
    result = "✓ Valid" if validate_url(url) else "✗ Invalid"
    print(f"   {result}: {url}")

# Example 4: IP Address validation
def validate_ip(ip):
    """
    Validate IPv4 address
    Pattern: 0-255.0-255.0-255.0-255
    """
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.fullmatch(pattern, ip) is not None

ips = [
    "192.168.1.1",    # Valid
    "10.0.0.255",     # Valid
    "255.255.255.0",  # Valid
    "256.1.1.1",      # Invalid - 256 > 255
    "192.168.1",      # Invalid - missing octet
    "192.168.1.1.1"   # Invalid - too many octets
]

print("\n4. IP ADDRESS VALIDATION:")
for ip in ips:
    result = "✓ Valid" if validate_ip(ip) else "✗ Invalid"
    print(f"   {result}: {ip}")

# Example 5: Date validation (YYYY-MM-DD)
def validate_date(date):
    """
    Validate date in YYYY-MM-DD format
    """
    pattern = r'^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
    return re.fullmatch(pattern, date) is not None

dates = [
    "2024-12-25",  # Valid
    "2023-01-01",  # Valid
    "2024-13-01",  # Invalid - month 13
    "2024-12-32",  # Invalid - day 32
    "24-12-25",    # Invalid - wrong year format
    "2024/12/25"   # Invalid - wrong separator
]

print("\n5. DATE VALIDATION (YYYY-MM-DD):")
for date in dates:
    result = "✓ Valid" if validate_date(date) else "✗ Invalid"
    print(f"   {result}: {date}")

# Example 6: Password strength validation
def validate_password(password):
    """
    Password requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    length_ok = len(password) >= 8
    has_upper = re.search(r'[A-Z]', password) is not None
    has_lower = re.search(r'[a-z]', password) is not None
    has_digit = re.search(r'\d', password) is not None
    has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None
    
    return all([length_ok, has_upper, has_lower, has_digit, has_special])

passwords = [
    "Secure123!",      # Valid
    "WeakPass",        # Invalid - no digit, no special
    "alllowercase1!",  # Invalid - no uppercase
    "ALLUPPERCASE1!",  # Invalid - no lowercase
    "NoSpecial123",    # Invalid - no special char
    "Short1!"          # Invalid - too short
]

print("\n6. PASSWORD STRENGTH VALIDATION:")
for pwd in passwords:
    result = "✓ Strong" if validate_password(pwd) else "✗ Weak"
    print(f"   {result}: {pwd}")

# Example 7: Username validation
def validate_username(username):
    """
    Username requirements:
    - 3-16 characters
    - Letters, numbers, underscore, hyphen
    - Must start with letter
    """
    pattern = r'^[a-zA-Z][a-zA-Z0-9_-]{2,15}$'
    return re.fullmatch(pattern, username) is not None

usernames = [
    "user123",      # Valid
    "john_doe",     # Valid
    "abc",          # Valid - minimum length
    "123user",      # Invalid - starts with digit
    "ab",           # Invalid - too short
    "user@name",    # Invalid - invalid character
]

print("\n7. USERNAME VALIDATION:")
for username in usernames:
    result = "✓ Valid" if validate_username(username) else "✗ Invalid"
    print(f"   {result}: {username}")

# Example 8: Credit card validation (format only, not checksum)
def validate_credit_card(card):
    """
    Validate credit card format
    Accepts: 1234-5678-9012-3456 or 1234567890123456
    """
    # Remove spaces and hyphens
    clean_card = re.sub(r'[\s-]', '', card)
    # Check if 13-19 digits
    pattern = r'^\d{13,19}$'
    return re.fullmatch(pattern, clean_card) is not None

cards = [
    "1234-5678-9012-3456",  # Valid
    "1234 5678 9012 3456",  # Valid
    "1234567890123456",     # Valid
    "1234-5678-9012",       # Invalid - too short
    "abcd-efgh-ijkl-mnop"   # Invalid - not digits
]

print("\n8. CREDIT CARD FORMAT VALIDATION:")
for card in cards:
    result = "✓ Valid" if validate_credit_card(card) else "✗ Invalid"
    print(f"   {result}: {card}")