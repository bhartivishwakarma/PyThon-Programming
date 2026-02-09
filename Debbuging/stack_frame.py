"""
CONCEPT: Stack Frame Inspection
- Examine the call stack at runtime
- Access local variables from calling functions
- Understand program execution flow
- Build advanced debugging tools

Call Stack:
Program execution creates a stack of function calls
Each call is a "frame" containing:
- Function name
- Local variables
- File location
- Line number

Uses:
1. Advanced debugging
2. Automatic logging
3. Profiling tools
4. Understanding code flow
"""

import inspect
import sys
from pprint import pprint

def show_call_stack():
    """
    Display detailed information about the current call stack
    """
    print("\n" + "="*70)
    print("CALL STACK ANALYSIS")
    print("="*70)
    
    # Get the current frame
    frame = inspect.currentframe()
    
    # Get all frames in the stack
    stack = inspect.stack()
    
    print(f"\nTotal frames in stack: {len(stack)}\n")
    
    for i, frame_info in enumerate(stack):
        print(f"{'─'*70}")
        print(f"Frame {i}: {frame_info.function}")
        print(f"{'─'*70}")
        print(f"  File: {frame_info.filename}")
        print(f"  Line: {frame_info.lineno}")
        print(f"  Function: {frame_info.function}")
        
        # Show code context
        if frame_info.code_context:
            print(f"  Code: {frame_info.code_context[0].strip()}")
        
        # Show local variables
        local_vars = frame_info.frame.f_locals
        print(f"  Local variables ({len(local_vars)}):")
        for var_name, var_value in local_vars.items():
            # Skip internal variables and large objects
            if not var_name.startswith('_'):
                value_str = str(var_value)
                if len(value_str) > 50:
                    value_str = value_str[:50] + "..."
                print(f"    {var_name} = {value_str} ({type(var_value).__name__})")
        
        print()

def get_caller_info():
    """
    Get information about the function that called this one
    """
    # stack()[0] is get_caller_info itself
    # stack()[1] is the function that called get_caller_info
    # stack()[2] is the function that called the caller
    
    caller_frame = inspect.stack()[1]
    
    print(f"\n{'='*70}")
    print("CALLER INFORMATION")
    print(f"{'='*70}")
    print(f"Called from function: {caller_frame.function}")
    print(f"File: {caller_frame.filename}")
    print(f"Line: {caller_frame.lineno}")
    print(f"Code: {caller_frame.code_context[0].strip() if caller_frame.code_context else 'N/A'}")
    
    # Access caller's local variables
    caller_locals = caller_frame.frame.f_locals
    print(f"\nCaller's local variables:")
    for name, value in caller_locals.items():
        if not name.startswith('_'):
            print(f"  {name} = {value}")

def trace_variable_origins(var_name):
    """
    Trace where a variable was defined in the call stack
    """
    print(f"\n{'='*70}")
    print(f"TRACING VARIABLE: '{var_name}'")
    print(f"{'='*70}")
    
    stack = inspect.stack()
    found_in_frames = []
    
    for i, frame_info in enumerate(stack):
        local_vars = frame_info.frame.f_locals
        if var_name in local_vars:
            found_in_frames.append({
                'frame_num': i,
                'function': frame_info.function,
                'file': frame_info.filename,
                'line': frame_info.lineno,
                'value': local_vars[var_name]
            })
    
    if found_in_frames:
        print(f"\nVariable '{var_name}' found in {len(found_in_frames)} frame(s):\n")
        for info in found_in_frames:
            print(f"Frame {info['frame_num']}: {info['function']}()")
            print(f"  Value: {info['value']}")
            print(f"  Location: {info['file']}:{info['line']}")
            print()
    else:
        print(f"\nVariable '{var_name}' not found in any frame")

def outer_function(x):
    """Outermost function"""
    y = x * 2
    print(f"\n>>> In outer_function: x={x}, y={y}")
    middle_function(y)

def middle_function(z):
    """Middle function"""
    w = z + 10
    print(f">>> In middle_function: z={z}, w={w}")
    inner_function(w)

def inner_function(a):
    """Innermost function"""
    b = a - 5
    c = b * 3
    print(f">>> In inner_function: a={a}, b={b}, c={c}")
    
    # Now show the call stack
    show_call_stack()
    
    # Show caller information
    get_caller_info()
    
    # Trace variable from outer scope
    trace_variable_origins('x')  # From outer_function
    trace_variable_origins('z')  # From middle_function
    trace_variable_origins('c')  # From inner_function

def advanced_stack_analysis():
    """
    Advanced stack frame analysis techniques
    """
    print("\n" + "="*70)
    print("ADVANCED STACK ANALYSIS")
    print("="*70)
    
    frame = inspect.currentframe()
    
    # Get information about this frame
    print(f"\nCurrent function: {inspect.getframeinfo(frame).function}")
    print(f"File: {inspect.getframeinfo(frame).filename}")
    print(f"Line: {inspect.getframeinfo(frame).lineno}")
    
    # Examine the code object
    code = frame.f_code
    print(f"\nCode object details:")
    print(f"  Arguments: {code.co_argcount}")
    print(f"  Local variables: {code.co_nlocals}")
    print(f"  Variable names: {code.co_varnames}")
    print(f"  Constants: {code.co_consts}")
    
    # Global and local namespace
    print(f"\nNamespace information:")
    print(f"  Globals: {len(frame.f_globals)} items")
    print(f"  Locals: {len(frame.f_locals)} items")
    print(f"  Builtins: {len(frame.f_builtins)} items")

def recursive_function(n, depth=0):
    """
    Demonstrate stack growth with recursion
    """
    if depth == 0:
        print(f"\n{'='*70}")
        print("RECURSIVE FUNCTION STACK ANALYSIS")
        print(f"{'='*70}")
    
    print(f"{'  ' * depth}Recursion depth: {depth}, n={n}")
    
    if n <= 0:
        # Base case - show stack
        stack_depth = len(inspect.stack())
        print(f"\n{'  ' * depth}Reached base case!")
        print(f"{'  ' * depth}Total stack depth: {stack_depth} frames")
        
        # Show just function names in stack
        print(f"\n{'  ' * depth}Call chain:")
        for i, frame in enumerate(inspect.stack()):
            indent = '  ' * (depth - i)
            print(f"{indent}{i}. {frame.function}()")
        
        return 0
    else:
        return recursive_function(n - 1, depth + 1) + n

# Demonstration
print("STACK FRAME INSPECTION DEMONSTRATION")
print("="*70)

print("\n1. Simple Call Stack Examination")
outer_function(5)

print("\n2. Advanced Stack Analysis")
advanced_stack_analysis()

print("\n3. Recursive Stack Growth")
result = recursive_function(5)
print(f"\nRecursive result: {result}")

print("\n" + "="*70)
print("STACK INSPECTION COMPLETE")
print("="*70)