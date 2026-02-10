"""
CONCEPT: Basic Regex Pattern Matching
- Literal characters match themselves
- Case-sensitive by default
- re.search() vs re.match() vs re.findall()

Basic Functions:
- re.search(pattern, string)  : Find first match anywhere
- re.match(pattern, string)   : Match from beginning only
- re.findall(pattern, string) : Find all matches
"""

import re

print("="*70)
print("Program 1: BASIC PATTERN MATCHING")
print("="*70)

# Example 1: Find word in sentence
text = "Python is a powerful programming language"
result = re.search("Python", text)

if result:
    print(f"\n✓ Found '{result.group()}' at position {result.start()}")
else:
    print("\n✗ Pattern not found")

# Example 2: Find all occurrences
text2 = "cat dog cat bird cat"
all_cats = re.findall("cat", text2)
print(f"\nFound 'cat' {len(all_cats)} times: {all_cats}")

# Example 3: Match from beginning
text3 = "Hello World"
if re.match("Hello", text3):
    print("\n✓ String starts with 'Hello'")

if not re.match("World", text3):
    print("✗ String does NOT start with 'World'")

# Example 4: Case-insensitive matching
text4 = "PYTHON Python python"
matches = re.findall("python", text4, re.IGNORECASE)
print(f"\nCase-insensitive matches: {matches}")

# Example 5: Practical use - check file extension
filename = "document.pdf"
if re.search(".pdf", filename):
    print(f"\n✓ '{filename}' is a PDF file")