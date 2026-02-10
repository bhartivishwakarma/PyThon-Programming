"""
CONCEPT: Quantifiers (Repetition)
Control how many times a pattern should repeat

Quantifiers:
*      - 0 or more times (greedy)
+      - 1 or more times (greedy)
?      - 0 or 1 time (optional)
{n}    - Exactly n times
{n,}   - n or more times
{n,m}  - Between n and m times

Greedy vs Non-greedy:
*  - Greedy (matches as much as possible)
*? - Non-greedy (matches as little as possible)
"""

import re

print("="*70)
print("Program 3: QUANTIFIERS (REPETITION)")
print("="*70)

# Example 1: * (zero or more)
text = "He said hmmm and hmm and hm"
pattern = r'hm*'  # h followed by zero or more m's
matches = re.findall(pattern, text)
print(f"\n1. Pattern 'hm*' matches: {matches}")

# Example 2: + (one or more)
text2 = "I have 1 apple, 23 oranges, and 456 grapes"
numbers = re.findall(r'\d+', text2)
print(f"\n2. Numbers (\\d+): {numbers}")

# Example 3: ? (optional - zero or one)
text3 = "color colour"
matches = re.findall(r'colou?r', text3)  # 'u' is optional
print(f"\n3. Pattern 'colou?r' matches: {matches}")

# Example 4: {n} - exactly n times
text4 = "File1 File22 File333 File4444"
three_digits = re.findall(r'File\d{3}', text4)
print(f"\n4. Files with exactly 3 digits: {three_digits}")

# Example 5: {n,} - n or more times
text5 = "aaa aa aaaa a aaaaa"
three_or_more = re.findall(r'a{3,}', text5)
print(f"\n5. 'a' repeated 3+ times: {three_or_more}")

# Example 6: {n,m} - between n and m times
text6 = "Phone: 123-4567 or 123-45-6789"
phone_parts = re.findall(r'\d{3,4}', text6)
print(f"\n6. Digit groups (3-4 digits): {phone_parts}")

# Example 7: Greedy vs Non-greedy
html = "<div>content</div><span>more</span>"
greedy = re.findall(r'<.*>', html)  # Greedy
non_greedy = re.findall(r'<.*?>', html)  # Non-greedy
print(f"\n7. Greedy '<.*>': {greedy}")
print(f"   Non-greedy '<.*?>': {non_greedy}")

# Example 8: Practical - validate password length
passwords = ["abc", "password", "secure123", "a"]
print(f"\n8. Password validation (8+ characters):")
for pwd in passwords:
    if re.fullmatch(r'.{8,}', pwd):
        print(f"   ✓ '{pwd}' - Valid")
    else:
        print(f"   ✗ '{pwd}' - Too short")

# Example 9: Extract repeated words
text7 = "Hello hello world WORLD"
repeated = re.findall(r'\b(\w+)\s+\1\b', text7, re.IGNORECASE)
print(f"\n9. Repeated words: {repeated}")

# Example 10: Match phone numbers
text8 = "Call 123-456-7890 or 987.654.3210"
phones = re.findall(r'\d{3}[-.]\d{3}[-.]\d{4}', text8)
print(f"\n10. Phone numbers: {phones}")