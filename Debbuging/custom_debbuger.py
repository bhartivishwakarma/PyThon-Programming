"""
CONCEPT: Debugger Decorators
- Function wrappers that add debugging behavior
- Non-invasive: don't change original function
- Reusable across multiple functions
- Can be toggled on/off
- Preserves function metadata with @functools.wraps

Decorator Pattern:
@decorator
def function():
    pass

Is equivalent to:
def function():
    pass
function = decorator(function)

Benefits:
1. Clean separation of debugging from business logic
2. Easy to enable/disable
3. Consistent debugging across functions
4. Composable (can stack multiple decorators)
"""

import functools
import time
from typing import Any

# Global flag to enable/disable debugging
DEBUG_ENABLED = True

def debug(func):
    """
    Decorator that logs function calls, arguments, return values, and exceptions
    """
    @functools.wraps(func)  # Preserves original function's metadata
    def wrapper(*args, **kwargs):
        if not DEBUG_ENABLED:
            return func(*args, **kwargs)
        
        # Format arguments for display
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        
        print(f"\n{'='*60}")
        print(f"Calling {func.__name__}({signature})")
        print(f"Function: {func.__module__}.{func.__name__}")
        
        try:
            # Call the actual function
            result = func(*args, **kwargs)
            
            print(f"{func.__name__} returned {result!r}")
            print(f"{'='*60}")
            
            return result
            
        except Exception as e:
            print(f"{func.__name__} raised {type(e).__name__}: {e}")
            print(f"{'='*60}")
            raise
    
    return wrapper

def timing_debug(func):
    """
    Decorator that measures and logs execution time
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not DEBUG_ENABLED:
            return func(*args, **kwargs)
        
        start_time = time.time()
        
        print(f"\n[TIMING] Starting {func.__name__}")
        result = func(*args, **kwargs)
        
        elapsed = time.time() - start_time
        print(f"[TIMING] {func.__name__} took {elapsed:.4f} seconds")
        
        return result
    
    return wrapper

def call_counter(func):
    """
    Decorator that counts how many times a function is called
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        print(f"[CALL #{wrapper.call_count}] {func.__name__}")
        return func(*args, **kwargs)
    
    wrapper.call_count = 0
    return wrapper

def validate_types(**type_hints):
    """
    Decorator factory that validates argument types
    
    Usage:
        @validate_types(x=int, y=int)
        def add(x, y):
            return x + y
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function's argument names
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            
            # Validate types
            for arg_name, expected_type in type_hints.items():
                if arg_name in bound_args.arguments:
                    value = bound_args.arguments[arg_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"{func.__name__}() argument '{arg_name}' must be "
                            f"{expected_type.__name__}, got {type(value).__name__}"
                        )
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

# Examples using the decorators

@debug
def calculate_power(base, exponent):
    """Calculate base raised to exponent"""
    return base ** exponent

@debug
@timing_debug
def fibonacci(n):
    """Calculate nth Fibonacci number (recursive)"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

@call_counter
@debug
def process_item(item):
    """Process a single item"""
    return item * 2

@validate_types(x=int, y=int)
@debug
def add_numbers(x, y):
    """Add two numbers with type validation"""
    return x + y

@debug
def divide_safely(a, b):
    """Division with error handling"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Demonstration
print("DECORATOR-BASED DEBUGGING EXAMPLES")
print("="*60)

print("\n1. Basic Function Debugging")
result = calculate_power(2, 3)
print(f"Result: {result}")

result = calculate_power(5, 0)
print(f"Result: {result}")

print("\n2. Recursive Function (shows call stack)")
print("Note: This will show all recursive calls")
result = fibonacci(5)
print(f"Final result: {result}")

print("\n3. Call Counter")
for i in range(3):
    process_item(i)
print(f"Total calls to process_item: {process_item.call_count}")

print("\n4. Type Validation")
try:
    result = add_numbers(10, 20)
    print(f"Valid addition result: {result}")
    
    print("\nTrying with invalid types:")
    result = add_numbers(10, "20")  # This will raise TypeError
except TypeError as e:
    print(f"Caught error: {e}")

print("\n5. Exception Handling in Decorator")
try:
    result = divide_safely(10, 0)
except ValueError as e:
    print(f"Caught exception: {e}")

print("\n6. Disabling Debug Mode")
DEBUG_ENABLED = False
print("DEBUG_ENABLED = False")
result = calculate_power(3, 3)  # No debug output
print(f"Result (no debug output): {result}")

print("\n7. Re-enabling Debug Mode")
DEBUG_ENABLED = True
print("DEBUG_ENABLED = True")
result = calculate_power(3, 3)  # Debug output returns
print(f"Result (with debug output): {result}")