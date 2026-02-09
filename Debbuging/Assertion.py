"""
CONCEPT: Assertions
- Verify assumptions in code
- Fail fast when preconditions aren't met
- Self-documenting code (shows what you expect)
- Should NOT replace proper exception handling in production
"""

def divide_numbers(a, b):
    # Precondition checks - verify inputs are valid before processing
    assert b != 0, "Divisor cannot be zero"
    assert isinstance(a, (int, float)), f"First argument must be a number, got {type(a)}"
    assert isinstance(b, (int, float)), f"Second argument must be a number, got {type(b)}"
    
    result = a / b
    
    # Postcondition check - verify result is reasonable
    assert isinstance(result, (int, float)), "Result should be a number"
    
    return result

# Valid test
result = divide_numbers(10, 2)
print(f"Valid division: {result}")

