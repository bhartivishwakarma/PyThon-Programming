"""
CONCEPT: ProcessPoolExecutor for parallel computing
LEARN: Using concurrent.futures with processes
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import math

def calculate_factorial(n):
    """Calculate factorial (CPU intensive)"""
    print(f"🔢 Calculating factorial of {n}")
    result = math.factorial(n)
    print(f"✓ {n}! has {len(str(result))} digits")
    return n, len(str(result))

def calculate_fibonacci(n):
    """Calculate nth Fibonacci number"""
    print(f"🔢 Calculating {n}th Fibonacci number")
    
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    print(f"✓ Fib({n}) calculated")
    return n, b

if __name__ == "__main__":
    print("=== PROCESS POOL FOR CALCULATIONS ===\n")
    
    # Tasks to compute
    factorial_numbers = [10000, 20000, 30000, 40000]
    fibonacci_numbers = [10000, 20000, 30000, 40000]
    
    print("Computing factorials in parallel...")
    start = time.time()
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Submit all factorial tasks
        factorial_futures = {
            executor.submit(calculate_factorial, n): n 
            for n in factorial_numbers
        }
        
        # Collect results as they complete
        for future in as_completed(factorial_futures):
            n, digit_count = future.result()
            print(f"  Result: {n}! has {digit_count} digits")
    
    factorial_time = time.time() - start
    print(f"Factorial time: {factorial_time:.2f}s\n")
    
    print("Computing Fibonacci in parallel...")
    start = time.time()
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Use map for simpler syntax
        results = executor.map(calculate_fibonacci, fibonacci_numbers)
        
        for n, fib_result in results:
            print(f"  Result: Fib({n}) calculated")
    
    fibonacci_time = time.time() - start
    print(f"Fibonacci time: {fibonacci_time:.2f}s")
    
    print(f"\n✓ All calculations complete!")

"""
OUTPUT:
=== PROCESS POOL FOR CALCULATIONS ===

Computing factorials in parallel...
🔢 Calculating factorial of 10000
🔢 Calculating factorial of 20000
🔢 Calculating factorial of 30000
🔢 Calculating factorial of 40000
✓ 10000! has 35660 digits
  Result: 10000! has 35660 digits
✓ 20000! has 77338 digits
  Result: 20000! has 77338 digits
...
Factorial time: 3.21s

Computing Fibonacci in parallel...
...
✓ All calculations complete!

KEY CONCEPTS:
✓ ProcessPoolExecutor - process-based parallel execution
✓ executor.submit() - submit single task
✓ executor.map() - map function to iterable
✓ Bypasses Python GIL for true parallelism
"""