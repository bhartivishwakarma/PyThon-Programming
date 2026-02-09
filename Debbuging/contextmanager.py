"""
CONCEPT: Context Managers for Debugging
- Automatic resource management
- Guaranteed cleanup (even with exceptions)
- Clean syntax with 'with' statement
- Useful for timing, logging, resource tracking

Structure:
with context_manager() as variable:
    # __enter__ runs here
    code block
    # __exit__ runs here (always, even if exception)

Benefits:
1. No manual cleanup needed
2. Exception-safe
3. Clean, readable code
4. Reusable debugging patterns
"""

import time
from contextlib import contextmanager
import sys

@contextmanager
def debug_timer(operation_name):
    """
    Context manager to measure and log execution time
    
    Usage:
        with debug_timer("My Operation"):
            # code to time
    """
    print(f"{'='*60}")
    print(f"Starting: {operation_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    start_memory = sys.getsizeof(locals())  # Rough memory estimate
    
    try:
        # This is where the 'with' block code runs
        yield  # Control passes to the with block
        
    except Exception as e:
        print(f"ERROR during {operation_name}: {e}")
        raise
        
    finally:
        # This always runs, even if exception occurred
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"{'='*60}")
        print(f"Finished: {operation_name}")
        print(f"Time taken: {elapsed:.4f} seconds")
        print(f"{'='*60}\n")

@contextmanager
def debug_section(section_name, verbose=True):
    """
    Context manager for debugging code sections
    Tracks entry, exit, and any exceptions
    """
    if verbose:
        print(f"\n>>> Entering: {section_name}")
    
    try:
        yield
        if verbose:
            print(f"<<< Exiting: {section_name} (Success)")
    except Exception as e:
        if verbose:
            print(f"<<< Exiting: {section_name} (Error: {e})")
        raise

@contextmanager
def variable_tracker(*var_names):
    """
    Context manager that tracks variable changes
    Must pass variables as locals() dict
    """
    print(f"\n--- Tracking variables: {', '.join(var_names)} ---")
    
    # Store initial state
    initial_state = {}
    
    yield initial_state  # Pass dict to with block
    
    # Show what changed
    print(f"--- Variable changes: ---")
    for name in var_names:
        if name in initial_state:
            print(f"{name}: {initial_state[name]}")

def slow_operation():
    """Example: Time a slow operation"""
    with debug_timer("Data Processing"):
        total = 0
        for i in range(1000000):
            total += i
        return total

def multi_step_process():
    """Example: Debug multiple sections"""
    result = 0
    
    with debug_section("Step 1: Initialize"):
        result = 10
        print(f"Initialized result to {result}")
    
    with debug_section("Step 2: Process"):
        result *= 5
        print(f"Processed result to {result}")
    
    with debug_section("Step 3: Finalize"):
        result += 100
        print(f"Finalized result to {result}")
    
    return result

def nested_operations():
    """Example: Nested context managers"""
    with debug_timer("Total Operation"):
        
        with debug_section("Part A"):
            time.sleep(0.5)
            print("Part A completed")
        
        with debug_section("Part B"):
            time.sleep(0.3)
            print("Part B completed")
        
        with debug_section("Part C"):
            time.sleep(0.2)
            print("Part C completed")

def error_handling_example():
    """Example: Context manager with exception"""
    try:
        with debug_timer("Operation with Error"):
            with debug_section("Before Error"):
                print("This works fine")
            
            with debug_section("Error Section"):
                print("About to cause error...")
                result = 10 / 0  # This will raise ZeroDivisionError
                
    except ZeroDivisionError:
        print("Exception was caught! Context managers still cleaned up properly.")

# Class-based context manager example
class DebugContext:
    """
    Class-based context manager for comparison
    Same as @contextmanager but more explicit
    """
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        print(f"[ENTER] {self.name}")
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        print(f"[EXIT] {self.name} (took {elapsed:.4f}s)")
        
        if exc_type:
            print(f"[EXCEPTION] {exc_type.__name__}: {exc_val}")
        
        return False  # Don't suppress exceptions

# Run examples
print("CONTEXT MANAGER DEBUGGING EXAMPLES")
print("="*60)

print("\n1. Simple Timer")
result = slow_operation()
print(f"Result: {result}")

print("\n2. Multi-Step Process")
result = multi_step_process()
print(f"Final result: {result}")

print("\n3. Nested Operations")
nested_operations()

print("\n4. Error Handling")
error_handling_example()

print("\n5. Class-based Context Manager")
with DebugContext("Class-based Example"):
    time.sleep(0.5)
    print("Doing some work...")