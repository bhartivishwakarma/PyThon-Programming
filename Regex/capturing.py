"""
CONCEPT: Groups and Capturing
Extract specific parts of matched patterns

Groups:
(...)           - Capturing group
(?:...)         - Non-capturing group (for grouping without capturing)
(?P<name>...)   - Named capturing group
\1, \2          - Backreference to group 1, 2, etc.

Group Methods:
match.group(0)  - Entire match
match.group(1)  - First group
match.groups()  - All groups as tuple
match.groupdict() - Named groups as dictionary
"""

import re

print("="*70)
print("Program 5: GROUPS AND CAPTURING")
print("="*70)

# Example 1: Basic capturing group
text = "John Smith is 25 years old"
match = re.search(r'(\w+) (\w+) is (\d+)', text)

if match:
    print(f"\n1. Full match: {match.group(0)}")
    print(f"   First name: {match.group(1)}")
    print(f"   Last name: {match.group(2)}")
    print(f"   Age: {match.group(3)}")
    print(f"   All groups: {match.groups()}")

# Example 2: Extract email parts
email = "username@example.com"
pattern = r'(\w+)@(\w+)\.(\w+)'
match = re.search(pattern, email)

if match:
    print(f"\n2. Email: {email}")
    print(f"   Username: {match.group(1)}")
    print(f"   Domain: {match.group(2)}")
    print(f"   TLD: {match.group(3)}")

# Example 3: Named groups
text2 = "Date: 2024-12-25"
pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
match = re.search(pattern, text2)

if match:
    print(f"\n3. Date parsing with named groups:")
    print(f"   Year: {match.group('year')}")
    print(f"   Month: {match.group('month')}")
    print(f"   Day: {match.group('day')}")
    print(f"   Dictionary: {match.groupdict()}")

# Example 4: Multiple matches with groups
text3 = "Contacts: John:123-4567, Jane:987-6543, Bob:555-1234"
pattern = r'(\w+):(\d{3}-\d{4})'
matches = re.findall(pattern, text3)

print(f"\n4. Extracted contacts:")
for name, phone in matches:
    print(f"   {name}: {phone}")

# Example 5: Non-capturing group (?:...)
text4 = "https://www.example.com and http://test.org"
# Capturing group
with_capture = re.findall(r'(https?)://(\w+\.\w+)', text4)
print(f"\n5. With capturing group: {with_capture}")

# Non-capturing group
without_capture = re.findall(r'(?:https?)://(\w+\.\w+)', text4)
print(f"   Non-capturing group: {without_capture}")

# Example 6: Backreferences - find repeated words
text5 = "hello hello world world world"
repeated = re.findall(r'\b(\w+)\s+\1\b', text5)
print(f"\n6. Repeated consecutive words: {repeated}")

# Example 7: Validate repeated patterns
html = "<div>content</div>"
if re.match(r'<(\w+)>.*</\1>', html):
    print(f"\n7. ✓ Valid HTML tag: {html}")

invalid_html = "<div>content</span>"
if not re.match(r'<(\w+)>.*</\1>', invalid_html):
    print(f"   ✗ Invalid HTML tag: {invalid_html}")

# Example 8: Extract and swap name parts
names = ["John Smith", "Jane Doe", "Bob Johnson"]
print(f"\n8. Name swapping (Last, First):")
for name in names:
    swapped = re.sub(r'(\w+) (\w+)', r'\2, \1', name)
    print(f"   {name} → {swapped}")

# Example 9: Parse log entries
log = "2024-12-25 10:30:45 [ERROR] Connection failed"
pattern = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) \[(\w+)\] (.+)'
match = re.search(pattern, log)

if match:
    print(f"\n9. Log parsing:")
    print(f"   Date: {match.group(1)}")
    print(f"   Time: {match.group(2)}")
    print(f"   Level: {match.group(3)}")
    print(f"   Message: {match.group(4)}")

# Example 10: Extract phone numbers with groups
text6 = "Call (123) 456-7890 or 987-654-3210"
pattern = r'\((\d{3})\)\s*(\d{3})-(\d{4})|(\d{3})-(\d{3})-(\d{4})'
matches = re.finditer(pattern, text6)

print(f"\n10. Phone numbers:")
for match in matches:
    print(f"    Full: {match.group(0)}")
    print(f"    Groups: {[g for g in match.groups() if g]}")