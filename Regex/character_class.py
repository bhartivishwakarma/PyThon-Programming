"""
CONCEPT: Character Classes
Special sequences that match categories of characters

Metacharacters:
\d - Any digit [0-9]
\D - Any non-digit
\w - Word character [a-zA-Z0-9_]
\W - Non-word character
\s - Whitespace (space, tab, newline)
\S - Non-whitespace
.  - Any character except newline
[abc] - Any character in brackets
[^abc] - Any character NOT in brackets
[a-z] - Range of characters
"""

import re

print("="*70)
print("Program 2: CHARACTER CLASSES")
print("="*70)

# Example 1: Extract all digits
text = "My phone number is 123-456-7890 and my age is 25"
digits = re.findall(r'\d', text)
print(f"\n1. All digits: {digits}")
print(f"   Joined: {''.join(digits)}")

# Example 2: Extract complete numbers (one or more digits)
numbers = re.findall(r'\d+', text)
print(f"\n2. All numbers: {numbers}")

# Example 3: Find word characters
text2 = "Hello_World123 @#$"
word_chars = re.findall(r'\w', text2)
print(f"\n3. Word characters: {word_chars}")
print(f"   Joined: {''.join(word_chars)}")

# Example 4: Find whitespace
text3 = "Hello\tWorld\nPython"
whitespace = re.findall(r'\s', text3)
print(f"\n4. Whitespace characters found: {len(whitespace)}")
print(f"   Text with visible whitespace: {repr(text3)}")

# Example 5: Match any character with dot (.)
pattern = r'c.t'  # c, any character, t
text4 = "cat cot cut cbt c9t"
matches = re.findall(pattern, text4)
print(f"\n5. Pattern 'c.t' matches: {matches}")

# Example 6: Character sets [abc]
text5 = "The quick brown fox jumps"
vowels = re.findall(r'[aeiou]', text5)
print(f"\n6. Vowels found: {vowels}")
print(f"   Count: {len(vowels)}")

# Example 7: Negated character set [^abc]
consonants = re.findall(r'[^aeiou\s]', text5.lower())
print(f"\n7. Consonants found: {consonants}")

# Example 8: Range [a-z] [0-9]
text6 = "ABC123xyz"
lowercase = re.findall(r'[a-z]', text6)
uppercase = re.findall(r'[A-Z]', text6)
print(f"\n8. Lowercase: {lowercase}")
print(f"   Uppercase: {uppercase}")

# Example 9: Practical - validate if string contains only digits
code = "12345"
if re.fullmatch(r'\d+', code):
    print(f"\n9. ✓ '{code}' contains only digits")

# Example 10: Extract alphanumeric words
text7 = "user123 @email.com test_var"
words = re.findall(r'\w+', text7)
print(f"\n10. Words extracted: {words}")