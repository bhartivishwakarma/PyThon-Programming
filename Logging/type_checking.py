"""
CONCEPT: Runtime Type Checking
- Verify data types before operations
- Catch type mismatches early
- Provide informative error messages
- Prevent cryptic runtime errors

type() vs isinstance():
- type(x) == int  -> Exact type match
- isinstance(x, int) -> Allows subclasses (better for OOP)
"""

def add_items(item1, item2):
    """
    Add two items with comprehensive type checking and debugging
    """
    # Debug: Show what we received
    print(f"Type of item1: {type(item1).__name__}, Value: {item1}")
    print(f"Type of item2: {type(item2).__name__}, Value: {item2}")
    
    # Check if both items are numbers
    if not isinstance(item1, (int, float)):
        raise TypeError(
            f"First item must be a number (int or float), "
            f"but got {type(item1).__name__}: {item1}"
        )
    
    if not isinstance(item2, (int, float)):
        raise TypeError(
            f"Second item must be a number (int or float), "
            f"but got {type(item2).__name__}: {item2}"
        )
    
    # If we reach here, types are valid
    result = item1 + item2
    print(f"Result type: {type(result).__name__}, Value: {result}")
    
    return result

def analyze_data_types(data):
    """
    Analyze and display information about various data types
    """
    print(f"\n--- Analyzing: {data} ---")
    print(f"Type: {type(data).__name__}")
    print(f"Is int? {isinstance(data, int)}")
    print(f"Is float? {isinstance(data, float)}")
    print(f"Is number? {isinstance(data, (int, float))}")
    print(f"Is string? {isinstance(data, str)}")
    print(f"Is list? {isinstance(data, list)}")

# Test valid inputs
print("=== Valid Addition ===")
result = add_items(5, 10)
print(f"5 + 10 = {result}\n")

result = add_items(5.5, 3.2)
print(f"5.5 + 3.2 = {result}\n")

# Test type analysis
analyze_data_types(42)
analyze_data_types(3.14)
analyze_data_types("hello")
analyze_data_types([1, 2, 3])

# Test invalid inputs (uncomment to see errors)
print("\n=== Invalid Addition (will raise TypeError) ===")
# add_items(5, "10")      # String instead of number
# add_items([1, 2], 5)    # List instead of number