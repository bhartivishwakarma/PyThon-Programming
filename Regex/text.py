"""
CONCEPT: Search and Replace with Regex
Transform text using pattern matching

Functions:
re.sub(pattern, replacement, string)   - Replace all matches
re.subn(pattern, replacement, string)  - Replace and return count
re.sub(pattern, function, string)      - Use function for replacement

Replacement Features:
\1, \2      - Backreferences to groups
\g<1>       - Alternative backreference syntax
\g<name>    - Named group reference
Function    - Dynamic replacement based on match
"""

import re

print("="*70)
print("Program 8: TEXT PROCESSING - SEARCH AND REPLACE")
print("="*70)

# Example 1: Simple replacement
text = "I love Python. Python is great. Python rocks!"
result = re.sub(r'Python', 'Java', text)
print(f"\n1. Simple replacement:")
print(f"   Original: {text}")
print(f"   Result:   {result}")

# Example 2: Case-insensitive replacement
text2 = "HELLO hello Hello"
result2 = re.sub(r'hello', 'Hi', text2, flags=re.IGNORECASE)
print(f"\n2. Case-insensitive:")
print(f"   Original: {text2}")
print(f"   Result:   {result2}")

# Example 3: Count replacements with subn()
text3 = "cat dog cat bird cat"
result3, count = re.subn(r'cat', 'mouse', text3)
print(f"\n3. Count replacements:")
print(f"   Original: {text3}")
print(f"   Result:   {result3}")
print(f"   Count:    {count} replacements")

# Example 4: Backreferences - swap words
text4 = "John Smith, Jane Doe, Bob Johnson"
result4 = re.sub(r'(\w+) (\w+)', r'\2, \1', text4)
print(f"\n4. Swap first and last names:")
print(f"   Original: {text4}")
print(f"   Result:   {result4}")

# Example 5: Redact sensitive information
text5 = "My SSN is 123-45-6789 and credit card is 1234-5678-9012-3456"
result5 = re.sub(r'\d{3}-\d{2}-\d{4}', 'XXX-XX-XXXX', text5)
result5 = re.sub(r'\d{4}-\d{4}-\d{4}-\d{4}', 'XXXX-XXXX-XXXX-XXXX', result5)
print(f"\n5. Redact sensitive data:")
print(f"   Original: {text5}")
print(f"   Result:   {result5}")

# Example 6: Remove HTML tags
html = "<p>This is <strong>bold</strong> and <em>italic</em> text.</p>"
result6 = re.sub(r'<[^>]+>', '', html)
print(f"\n6. Remove HTML tags:")
print(f"   Original: {html}")
print(f"   Result:   {result6}")

# Example 7: Normalize whitespace
text7 = "Too    many     spaces   and\ttabs\nand\nnewlines"
result7 = re.sub(r'\s+', ' ', text7)
print(f"\n7. Normalize whitespace:")
print(f"   Original: {repr(text7)}")
print(f"   Result:   {result7}")

# Example 8: Function as replacement
def uppercase_match(match):
    """Convert matched text to uppercase"""
    return match.group(0).upper()

text8 = "make these words LOUD: hello world python"
result8 = re.sub(r'\b\w+\b', uppercase_match, text8)
print(f"\n8. Function replacement (uppercase):")
print(f"   Original: {text8}")
print(f"   Result:   {result8}")

# Example 9: Add prefix to numbers
def add_dollar(match):
    """Add dollar sign to numbers"""
    return f"${match.group(0)}"

text9 = "Prices: 10, 25.50, and 100"
result9 = re.sub(r'\d+\.?\d*', add_dollar, text9)
print(f"\n9. Add currency symbol:")
print(f"   Original: {text9}")
print(f"   Result:   {result9}")

# Example 10: Censor bad words
def censor_word(match):
    """Replace word with asterisks of same length"""
    word = match.group(0)
    return '*' * len(word)

text10 = "This badword is not allowed and anotherword too"
bad_words = r'\b(badword|anotherword)\b'
result10 = re.sub(bad_words, censor_word, text10)
print(f"\n10. Censor bad words:")
print(f"    Original: {text10}")
print(f"    Result:   {result10}")

# Example 11: Format phone numbers
text11 = "Call 1234567890 or 9876543210"
result11 = re.sub(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', text11)
print(f"\n11. Format phone numbers:")
print(f"    Original: {text11}")
print(f"    Result:   {result11}")

# Example 12: Convert markdown links to HTML
text12 = "Check [Google](http://google.com) and [Python](http://python.org)"
result12 = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text12)
print(f"\n12. Markdown to HTML links:")
print(f"    Original: {text12}")
print(f"    Result:   {result12}")

# Example 13: Camel case to snake case
def camel_to_snake(match):
    """Convert camelCase to snake_case"""
    return '_' + match.group(0).lower()

text13 = "myVariableName and anotherVariable"
result13 = re.sub(r'(?<!^)(?=[A-Z])', '_', text13).lower()
print(f"\n13. CamelCase to snake_case:")
print(f"    Original: {text13}")
print(f"    Result:   {result13}")