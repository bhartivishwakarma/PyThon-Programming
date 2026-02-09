"""
CONCEPT: Print Debugging
- Simplest form of debugging
- Tracks program execution flow
- Shows variable values at different points
- Use descriptive labels for clarity
"""

def calculate_average(numbers):
    # Print input to verify what data we're receiving
    print(f"Input numbers: {numbers}")
    
    total = sum(numbers)
    print(f"Total: {total}")  # Track intermediate calculation
    
    count = len(numbers)
    print(f"Count: {count}")  # Verify count is correct
    
    average = total / count
    print(f"Average: {average}")  # Final result before return
    
    return average

# Test the function
calculate_average([10, 20, 30, 40])

