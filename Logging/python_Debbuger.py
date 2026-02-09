"""
CONCEPT: Python Debugger (pdb)
- Interactive debugging tool
- Pause execution at any point
- Inspect variables in real-time
- Step through code line by line
- Modify variables during execution

HOW TO USE:
1. Run the program
2. When pdb.set_trace() is hit, execution pauses
3. Use commands to navigate and inspect
4. Type 'help' in debugger for command list

COMMON COMMANDS:
n (next)     - Execute current line, move to next
s (step)     - Step into function calls
c (continue) - Continue execution until next breakpoint
p var        - Print variable value
l (list)     - Show code context
w (where)    - Show call stack
q (quit)     - Exit debugger
"""

import pdb

def complex_calculation(x, y, z):
    """
    Perform multi-step calculation with debugging
    
    Try these commands when debugger pauses:
    - p x          (print value of x)
    - p locals()   (print all local variables)
    - n            (execute next line)
    - l            (show code context)
    - w            (show where you are in call stack)
    """
    
    print(f"Starting calculation with x={x}, y={y}, z={z}")
    
    # Breakpoint - execution will pause here
    pdb.set_trace()  # <-- Debugger will stop at this line
    
    step1 = x + y
    print(f"Step 1: {x} + {y} = {step1}")
    
    step2 = step1 * z
    print(f"Step 2: {step1} * {z} = {step2}")
    
    step3 = step2 - x
    print(f"Step 3: {step2} - {x} = {step3}")
    
    final = step3 / y
    print(f"Final: {step3} / {y} = {final}")
    
    return final

def debug_loop_example():
    """
    Example with loop and conditional debugging
    """
    numbers = [1, 2, 3, 4, 5]
    results = []
    
    for i, num in enumerate(numbers):
        # Conditional breakpoint - only pause when num is 3
        if num == 3:
            pdb.set_trace()  # Will only pause when num == 3
        
        squared = num ** 2
        results.append(squared)
        print(f"Iteration {i}: {num}^2 = {squared}")
    
    return results

# Example usage instructions
print("""
PDB DEBUGGER EXAMPLE
====================

This program demonstrates pdb (Python Debugger).

INSTRUCTIONS:
1. Uncomment ONE of the function calls below
2. Run the program
3. When it pauses, try these commands:
   - 'p step1'  : print variable value
   - 'n'        : next line
   - 's'        : step into function
   - 'l'        : list code around current line
   - 'c'        : continue execution
   - 'q'        : quit debugger

Try it now!
""")

# Uncomment one of these to try debugging:
# result = complex_calculation(10, 5, 3)
# result = debug_loop_example()

# Alternative: Use breakpoint() (Python 3.7+)
# breakpoint() is equivalent to pdb.set_trace()
def modern_debugging_example(a, b):
    """Using Python 3.7+ breakpoint() function"""
    print(f"Inputs: a={a}, b={b}")
    
    # Modern way to set breakpoint
    breakpoint()  # Same as pdb.set_trace() but more flexible
    
    result = a * b + a / b
    return result

# Uncomment to try:
# modern_debugging_example(10, 5)

print("\nNote: Uncomment a function call above to start debugging!")