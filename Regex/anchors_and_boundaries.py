"""
CONCEPT: Anchors and Boundaries
Specify position in the string, not characters

Anchors:
^  - Start of string (or line with re.MULTILINE)
$  - End of string (or line with re.MULTILINE)
\b - Word boundary (between \w and \W)
\B - Non-word boundary
\A - Start of string (absolute)
\Z - End of string (absolute)

Word Boundary \b:
- Matches position between word and non-word character
- Useful for whole word matching
"""

import re

print("="*70)
print("Program 4: ANCHORS AND BOUNDARIES")
print("="*70)

# Example 1: ^ Start of string
text = "Python is great. Python programming is fun."
start_match = re.findall(r'^Python', text)
print(f"\n1. Matches at start (^Python): {start_match}")

all_python = re.findall(r'Python', text)
print(f"   All 'Python' occurrences: {all_python}")

# Example 2: $ End of string
emails = ["user@example.com", "admin@test.org", "info@site.net"]
print(f"\n2. Emails ending with '.com':")
for email in emails:
    if re.search(r'\.com$', email):
        print(f"   ✓ {email}")
    else:
        print(f"   ✗ {email}")

# Example 3: \b Word boundary
text2 = "cat catch scatter wildcat"
whole_word = re.findall(r'\bcat\b', text2)
partial = re.findall(r'cat', text2)
print(f"\n3. Text: '{text2}'")
print(f"   Whole word '\\bcat\\b': {whole_word}")
print(f"   Partial 'cat': {partial}")

# Example 4: Extract whole words only
text3 = "The number is 123 and 123abc and abc123"
whole_numbers = re.findall(r'\b\d+\b', text3)
print(f"\n4. Whole numbers only: {whole_numbers}")

# Example 5: \B Non-word boundary
text4 = "cat catch scatter wildcat"
non_boundary = re.findall(r'\Bcat', text4)
print(f"\n5. 'cat' NOT at word boundary: {non_boundary}")

# Example 6: Validate username (start to end)
usernames = ["user123", "123user", "user_name", "user-name"]
print(f"\n6. Valid usernames (letters/digits/underscore only):")
for username in usernames:
    if re.fullmatch(r'^\w+$', username):
        print(f"   ✓ {username}")
    else:
        print(f"   ✗ {username}")

# Example 7: Multiline mode with ^ and $
multiline_text = """First line
Second line
Third line"""

# Without MULTILINE - matches only at start/end of entire string
without_ml = re.findall(r'^.*$', multiline_text)
print(f"\n7. Without MULTILINE: {without_ml}")

# With MULTILINE - matches at start/end of each line
with_ml = re.findall(r'^.*$', multiline_text, re.MULTILINE)
print(f"   With MULTILINE: {with_ml}")

# Example 8: Extract sentences (end with period)
text5 = "Hello. How are you? I am fine. Great!"
sentences = re.findall(r'[^.!?]+[.!?]', text5)
print(f"\n8. Sentences: {sentences}")

# Example 9: Validate line format
lines = ["Name: John", "Age: 25", "Invalid line", "City: NYC"]
print(f"\n9. Lines in 'Key: Value' format:")
for line in lines:
    if re.match(r'^\w+:\s*.+$', line):
        print(f"   ✓ {line}")
    else:
        print(f"   ✗ {line}")

# Example 10: Extract hashtags (word boundaries)
tweet = "#Python is #awesome! Learn #programming today. #Python123"
hashtags = re.findall(r'#\w+', tweet)
print(f"\n10. Hashtags: {hashtags}")

# Whole hashtag words only
proper_hashtags = re.findall(r'\B#\w+', tweet)
print(f"    Proper hashtags: {proper_hashtags}")