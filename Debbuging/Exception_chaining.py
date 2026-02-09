"""
CONCEPT: Exception Chaining
- Link related exceptions together
- Preserve original error context
- Show complete error history
- Better error messages in complex systems

Exception Attributes:
- __cause__   : Explicit exception cause (using 'from')
- __context__ : Implicit exception context (automatic)
- __traceback__: Stack trace information

Syntax:
raise NewException("message") from original_exception

Benefits:
1. Complete error history
2. Root cause identification
3. Better debugging information
4. Clearer error messages
"""

# Define custom exception hierarchy
class ApplicationError(Exception):
    """Base exception for application"""
    pass

class DatabaseError(ApplicationError):
    """Database-related errors"""
    pass

class ConnectionError(DatabaseError):
    """Connection failures"""
    pass

class QueryError(DatabaseError):
    """Query execution failures"""
    pass

class ValidationError(ApplicationError):
    """Data validation failures"""
    pass

class BusinessLogicError(ApplicationError):
    """Business rule violations"""
    pass

def connect_to_database(host, port):
    """
    Simulate database connection failure
    """
    print(f"Attempting to connect to {host}:{port}...")
    # Simulate connection failure
    raise ConnectionError(f"Failed to connect to database at {host}:{port}")

def execute_query(query):
    """
    Execute database query with exception chaining
    """
    print(f"Executing query: {query}")
    
    try:
        # Try to connect
        connect_to_database("localhost", 5432)
        
    except ConnectionError as e:
        # Wrap the connection error in a query error
        # The 'from e' preserves the original exception
        raise QueryError(f"Query failed: {query}") from e

def fetch_user_data(user_id):
    """
    Fetch user data with multiple exception layers
    """
    print(f"\nFetching data for user {user_id}...")
    
    try:
        query = f"SELECT * FROM users WHERE id={user_id}"
        execute_query(query)
        
    except QueryError as e:
        # Add another layer to the exception chain
        raise ValidationError(f"Could not validate user {user_id}") from e

def process_user_request(user_id):
    """
    Process user request with complete exception chain
    """
    print(f"\n{'='*70}")
    print(f"Processing request for user {user_id}")
    print(f"{'='*70}")
    
    try:
        user_data = fetch_user_data(user_id)
        return user_data
        
    except ValidationError as e:
        print(f"\n{'!'*70}")
        print("EXCEPTION CHAIN ANALYSIS")
        print(f"{'!'*70}")
        
        # Show the top-level exception
        print(f"\nTop-level Exception:")
        print(f"  Type: {type(e).__name__}")
        print(f"  Message: {e}")
        
        # Show the explicit cause (__cause__)
        if e.__cause__:
            print(f"\nExplicit Cause (__cause__):")
            print(f"  Type: {type(e.__cause__).__name__}")
            print(f"  Message: {e.__cause__}")
        
        # Walk the entire exception chain
        print(f"\nComplete Exception Chain:")
        current = e
        level = 1
        
        while current:
            print(f"\n  Level {level}: {type(current).__name__}")
            print(f"  Message: {current}")
            
            if current.__cause__:
                current = current.__cause__
            elif current.__context__:
                current = current.__context__
            else:
                current = None
            
            level += 1
        
        # Show traceback
        print(f"\n{'─'*70}")
        print("Full Traceback:")
        print(f"{'─'*70}")
        import traceback
        traceback.print_exc()
        
        return None

def demonstrate_implicit_chaining():
    """
    Demonstrate implicit exception chaining (__context__)
    """
    print(f"\n{'='*70}")
    print("IMPLICIT EXCEPTION CHAINING")
    print(f"{'='*70}")
    
    try:
        try:
            # First exception
            x = 1 / 0
        except ZeroDivisionError:
            # Second exception (different error)
            # This automatically chains to the first
            y = int("not a number")
    
    except ValueError as e:
        print(f"\nCurrent Exception: {type(e).__name__}: {e}")
        
        # __context__ is automatically set
        if e.__context__:
            print(f"Context Exception: {type(e.__context__).__name__}: {e.__context__}")
        
        print("\nNote: __context__ is set automatically when an exception")
        print("occurs while handling another exception")

def demonstrate_suppressing_context():
    """
    Demonstrate suppressing exception context with 'from None'
    """
    print(f"\n{'='*70}")
    print("SUPPRESSING EXCEPTION CONTEXT")
    print(f"{'='*70}")
    
    try:
        try:
            result = 10 / 0
        except ZeroDivisionError:
            # 'from None' suppresses the original exception
            raise ValueError("Invalid calculation") from None
    
    except ValueError as e:
        print(f"\nException: {e}")
        print(f"__cause__: {e.__cause__}")
        print(f"__context__: {e.__context__}")
        print("\nUsing 'from None' suppresses the original exception")

def multi_layer_application():
    """
    Simulate a multi-layer application with exception chaining
    """
    print(f"\n{'='*70}")
    print("MULTI-LAYER APPLICATION ERROR HANDLING")
    print(f"{'='*70}")
    
    def data_layer():
        """Lowest layer - data access"""
        raise ConnectionError("Database connection timeout")
    
    def business_layer():
        """Middle layer - business logic"""
        try:
            data_layer()
        except ConnectionError as e:
            raise BusinessLogicError("Failed to process business rule") from e
    
    def presentation_layer():
        """Top layer - user interface"""
        try:
            business_layer()
        except BusinessLogicError as e:
            raise ApplicationError("Application failed to complete request") from e
    
    try:
        presentation_layer()
    except ApplicationError as e:
        print("\nApplication Error Occurred!")
        print("\nError Stack (top to bottom):")
        
        current = e
        depth = 0
        while current:
            indent = "  " * depth
            print(f"{indent}↓ {type(current).__name__}: {current}")
            current = current.__cause__
            depth += 1
        
        print("\nThis shows the complete path of the error through all layers")

def custom_exception_with_debugging_info():
    """
    Custom exception that includes debugging information
    """
    print(f"\n{'='*70}")
    print("CUSTOM EXCEPTION WITH DEBUGGING INFO")
    print(f"{'='*70}")
    
    class DetailedError(Exception):
        """Exception with rich debugging information"""
        def __init__(self, message, **debug_info):
            super().__init__(message)
            self.debug_info = debug_info
        
        def __str__(self):
            base = super().__str__()
            if self.debug_info:
                debug_str = "\n  Debug Info:\n"
                for key, value in self.debug_info.items():
                    debug_str += f"    {key}: {value}\n"
                return base + debug_str
            return base
    
    try:
        try:
            data = {"user": "alice", "age": "invalid"}
            age = int(data["age"])
        except ValueError as e:
            raise DetailedError(
                "Failed to process user data",
                user=data["user"],
                invalid_field="age",
                invalid_value=data["age"],
                expected_type="integer"
            ) from e
    
    except DetailedError as e:
        print(f"\nError occurred:")
        print(f"{e}")
        print(f"\nOriginal cause: {e.__cause__}")

# Run all demonstrations
print("EXCEPTION CHAINING DEMONSTRATION")
print("="*70)

# Main demonstration
process_user_request(123)

# Additional demonstrations
demonstrate_implicit_chaining()
demonstrate_suppressing_context()
multi_layer_application()
custom_exception_with_debugging_info()

print("\n" + "="*70)
print("EXCEPTION CHAINING COMPLETE")
print("="*70)