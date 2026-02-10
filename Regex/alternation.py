"""
CONCEPT: Alternation (OR Operator)
Match one pattern OR another

Syntax:
pattern1|pattern2|pattern3

Usage:
- cat|dog        : Matches 'cat' or 'dog'
- (jpg|png|gif)  : Matches any image extension
- Mr\.|Mrs\.|Ms\.: Matches title prefixes

Priority:
- Alternation has low priority
- Use parentheses for grouping
- Matches left to right (first match wins)
"""

import re

print("="*70)
print("Program 6: ALTERNATION (OR OPERATOR)")
print("="*70)

# Example 1: Simple OR
text = "I have a cat and a dog"
pets = re.findall(r'cat|dog', text)
print(f"\n1. Pets found: {pets}")

# Example 2: Multiple alternatives
text2 = "Fruits: apple, banana, cherry, orange"
fruits = re.findall(r'apple|banana|cherry', text2)
print(f"\n2. Matched fruits: {fruits}")

# Example 3: With word boundaries
text3 = "cat catch scatter"
whole_words = re.findall(r'\b(cat|dog)\b', text3)
print(f"\n3. Whole word matches: {whole_words}")

# Example 4: File extensions
files = ["image.jpg", "document.pdf", "photo.png", "video.mp4", "picture.gif"]
images = [f for f in files if re.search(r'\.(jpg|png|gif)$', f)]
print(f"\n4. Image files: {images}")

# Example 5: Match title prefixes
names = ["Mr. Smith", "Mrs. Johnson", "Ms. Davis", "Dr. Brown"]
pattern = r'(Mr\.|Mrs\.|Ms\.|Dr\.)\s+(\w+)'

print(f"\n5. Names with titles:")
for name in names:
    match = re.search(pattern, name)
    if match:
        print(f"   Title: {match.group(1)}, Name: {match.group(2)}")

# Example 6: Protocol matching
urls = ["http://example.com", "https://secure.com", "ftp://files.net"]
http_urls = [url for url in urls if re.match(r'https?://', url)]
print(f"\n6. HTTP/HTTPS URLs: {http_urls}")

# Example 7: Color codes (name or hex)
text4 = "Colors: red #FF0000 blue #0000FF green"
colors = re.findall(r'\b(red|blue|green|#[0-9A-Fa-f]{6})\b', text4)
print(f"\n7. Colors: {colors}")

# Example 8: Multiple date formats
dates = ["2024-12-25", "12/25/2024", "25.12.2024"]
pattern = r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{2}\.\d{2}\.\d{4}'

print(f"\n8. Valid dates:")
for date in dates:
    if re.fullmatch(pattern, date):
        print(f"   ✓ {date}")

# Example 9: Programming languages
text5 = "I know Python, Java, and JavaScript. Also learning C++ and C#"
languages = re.findall(r'\b(Python|Java(?:Script)?|C\+\+|C#)\b', text5)
print(f"\n9. Programming languages: {languages}")

# Example 10: Validate yes/no responses
responses = ["yes", "Yes", "YES", "no", "NO", "maybe"]
print(f"\n10. Valid yes/no responses:")
for response in responses:
    if re.fullmatch(r'(?i)(yes|no)', response):  # (?i) for case-insensitive
        print(f"    ✓ {response}")
    else:
        print(f"    ✗ {response}")

# Example 11: Email or phone
contacts = ["user@example.com", "123-456-7890", "admin@test.org", "555-1234"]
email_or_phone = r'\w+@\w+\.\w+|\d{3}-\d{3}-\d{4}'

print(f"\n11. Contacts (email or phone):")
for contact in contacts:
    if re.fullmatch(email_or_phone, contact):
        if '@' in contact:
            print(f"    Email: {contact}")
        else:
            print(f"    Phone: {contact}")

# Example 12: Priority demonstration
text6 = "catdog"
# First match wins
first_match = re.search(r'cat|catdog', text6)
print(f"\n12. Priority test (cat|catdog): '{first_match.group()}'")

second_match = re.search(r'catdog|cat', text6)
print(f"    Priority test (catdog|cat): '{second_match.group()}'")