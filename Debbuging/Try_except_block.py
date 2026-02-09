"""
CONCEPT: Exception Handling
- Prevents program crashes
- Provides graceful error recovery
- Gives detailed error information
- Separates normal code from error handling
"""

def safe_list_access(lst, index):
    """
    Safely access list elements with proper error handling
    """
    try:
        # Attempt the operation that might fail
        element = lst[index]
        print(f"Successfully retrieved: {element}")
        return element
        
    except IndexError as e:
        # Handle specific exception type
        print(f"IndexError caught: {e}")
        print(f"Debug info - List length: {len(lst)}, Index requested: {index}")
        return None
        
    except TypeError as e:
        # Handle different exception type
        print(f"TypeError caught: {e}")
        print("Make sure you're passing a list and an integer index")
        return None
        
    finally:
        # This always executes, regardless of exceptions
        print(f"Access attempt completed for index {index}")

# Test cases
my_list = [1, 2, 3, 4, 5]

print("\n--- Test 1: Valid access ---")
safe_list_access(my_list, 2)

print("\n--- Test 2: Index out of range ---")
safe_list_access(my_list, 10)

print("\n--- Test 3: Invalid index type ---")
