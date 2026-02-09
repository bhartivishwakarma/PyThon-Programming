"""
CONCEPT: Custom Exceptions
- Create domain-specific exception types
- Store debugging context with the exception
- Provide structured error information
- Make error handling more precise
- Better error messages for debugging

Benefits:
1. Clear error categorization
2. Additional debugging context
3. Easier to catch specific errors
4. Self-documenting code
"""

class DataValidationError(Exception):
    """
    Custom exception for data validation failures
    Stores additional context for debugging
    """
    def __init__(self, message, data, expected_type, field_name=None):
        self.message = message
        self.data = data
        self.expected_type = expected_type
        self.field_name = field_name
        
        # Create detailed error message
        full_message = f"{message}\n"
        if field_name:
            full_message += f"Field: {field_name}\n"
        full_message += f"Expected: {expected_type.__name__}\n"
        full_message += f"Received: {type(data).__name__} = {data}"
        
        super().__init__(full_message)

class ProcessingError(Exception):
    """Exception for processing failures"""
    pass

def validate_data(data, expected_type, field_name="data"):
    """
    Validate data type and raise custom exception if invalid
    """
    print(f"Validating {field_name}: {data} (type: {type(data).__name__})")
    
    if not isinstance(data, expected_type):
        raise DataValidationError(
            message=f"Invalid data type for {field_name}",
            data=data,
            expected_type=expected_type,
            field_name=field_name
        )
    
    print(f"✓ Validation passed for {field_name}")
    return True

def process_user_input(user_data):
    """
    Process user input with multiple validation steps
    """
    try:
        # Validate each field
        validate_data(user_data.get('age'), int, 'age')
        validate_data(user_data.get('name'), str, 'name')
        validate_data(user_data.get('email'), str, 'email')
        
        print("All validations passed! Processing data...")
        return {"status": "success", "data": user_data}
        
    except DataValidationError as e:
        # Custom exception provides rich debugging info
        print(f"\n{'='*50}")
        print("VALIDATION ERROR DETAILS:")
        print(f"{'='*50}")
        print(f"Error Message: {e.message}")
        print(f"Field Name: {e.field_name}")
        print(f"Received Data: {e.data} (type: {type(e.data).__name__})")
        print(f"Expected Type: {e.expected_type.__name__}")
        print(f"{'='*50}\n")
        
        return {"status": "error", "error": str(e)}

# Test cases
print("--- Test 1: Valid data ---")
valid_user = {
    'age': 25,
    'name': 'Alice',
    'email': 'alice@example.com'
}
process_user_input(valid_user)

print("\n--- Test 2: Invalid age (string instead of int) ---")
invalid_user = {
    'age': "25",  # Should be int
    'name': 'Bob',
    'email': 'bob@example.com'
}
process_user_input(invalid_user)

print("\n--- Test 3: Invalid name (int instead of string) ---")
invalid_user2 = {
    'age': 30,
    'name': 12345,  # Should be string
    'email': 'charlie@example.com'
}
process_user_input(invalid_user2)