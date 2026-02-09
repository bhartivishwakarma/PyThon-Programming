"""
CONCEPT: Logging
- Professional alternative to print statements
- Five severity levels for different message types
- Configurable output format and destination
- Can be filtered by level
- Persistent across application

LOGGING LEVELS:
DEBUG    - Detailed diagnostic information
INFO     - Confirmation things are working
WARNING  - Something unexpected, but still working
ERROR    - Serious problem, function failed
CRITICAL - Very serious, program may crash
"""

import logging

# Configure logging (do this once at program start)
logging.basicConfig(
    level=logging.DEBUG,  # Show all messages at DEBUG level and above
    format='%(levelname)s: %(message)s'  # Format: LEVEL: message
)

def process_data(data):
    """Process data with comprehensive logging"""
    
    # DEBUG: Detailed information for diagnosing problems
    logging.debug(f"Starting to process data: {data}")
    logging.debug(f"Data type: {type(data)}, Length: {len(data)}")
    
    # INFO: Confirmation that things are working as expected
    logging.info("Processing in progress")
    
    # Perform the actual processing
    result = [x * 2 for x in data]
    
    # DEBUG: Show the result for verification
    logging.debug(f"Result: {result}")
    
    # INFO: Successful completion
    logging.info(f"Successfully processed {len(data)} items")
    
    return result

def risky_operation(value):
    """Demonstrate WARNING, ERROR, and CRITICAL levels"""
    
    if value < 0:
        # WARNING: Something unexpected but not critical
        logging.warning(f"Negative value received: {value}. Using absolute value.")
        value = abs(value)
    
    try:
        result = 100 / value
        return result
    except ZeroDivisionError:
        # ERROR: Serious problem, function failed
        logging.error(f"Cannot divide by zero! Input was: {value}")
        return None
    except Exception as e:
        # CRITICAL: Very serious error
        logging.critical(f"Unexpected critical error: {e}")
        raise

# Test the functions
print("--- Processing normal data ---")
process_data([1, 2, 3, 4, 5])

print("\n--- Risky operations ---")
risky_operation(10)      # Normal
risky_operation(-5)      # Warning
risky_operation(0)       # Error