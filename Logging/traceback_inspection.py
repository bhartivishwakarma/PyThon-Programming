"""
CONCEPT: Traceback Inspection
- Examine the call stack when errors occur
- Understand the sequence of function calls
- Extract detailed debugging information
- Log errors with full context

Traceback Components:
1. Stack frames - Each function call
2. File and line numbers - Where code executed
3. Code context - The actual code that ran
4. Exception type and message
"""

import traceback
import sys

def level_3_deepest():
    """Innermost function where error occurs"""
    print("Executing level_3_deepest()")
    x = 10
    y = 0
    # This will cause ZeroDivisionError
    return x / y

def level_2_middle(value):
    """Middle function in call chain"""
    print(f"Executing level_2_middle({value})")
    result = level_3_deepest()
    return result * 2

def level_1_outer(initial_value):
    """Outermost function"""
    print(f"Executing level_1_outer({initial_value})")
    processed = level_2_middle(initial_value)
    return processed + 100

def demonstrate_traceback():
    """
    Demonstrate comprehensive traceback inspection
    """
    print("="*60)
    print("TRACEBACK INSPECTION DEMONSTRATION")
    print("="*60)
    
    try:
        result = level_1_outer(5)
        
    except Exception as e:
        print("\n--- BASIC EXCEPTION INFO ---")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        
        print("\n--- EXCEPTION DETAILS (sys.exc_info) ---")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f"Type: {exc_type}")
        print(f"Value: {exc_value}")
        print(f"Traceback object: {exc_traceback}")
        
        print("\n--- FORMATTED TRACEBACK ---")
        traceback.print_exc()
        
        print("\n--- DETAILED TRACEBACK ANALYSIS ---")
        tb_lines = traceback.format_tb(exc_traceback)
        for i, line in enumerate(tb_lines, 1):
            print(f"Frame {i}:")
            print(line)
        
        print("\n--- TRACEBACK FRAME DETAILS ---")
        tb = exc_traceback
        frame_number = 1
        while tb is not None:
            frame = tb.tb_frame
            print(f"\nFrame {frame_number}:")
            print(f"  Function: {frame.f_code.co_name}")
            print(f"  File: {frame.f_code.co_filename}")
            print(f"  Line: {tb.tb_lineno}")
            print(f"  Local variables: {frame.f_locals}")
            
            tb = tb.tb_next
            frame_number += 1
        
        print("\n--- FORMATTED EXCEPTION STRING ---")
        exception_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print(exception_str)

# Run the demonstration
demonstrate_traceback()