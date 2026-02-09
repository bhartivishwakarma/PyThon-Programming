"""
CONCEPT: Advanced File Logging
- Production-ready logging configuration
- Persistent logs for later analysis
- Timestamp tracking for chronological debugging
- Multiple handlers for different outputs
- Log levels filter message importance

LOG LEVELS (lowest to highest):
DEBUG    (10) - Detailed diagnostic info
INFO     (20) - General information
WARNING  (30) - Warning messages
ERROR    (40) - Error messages
CRITICAL (50) - Critical errors

Only messages at or above the configured level are logged.
"""

import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging with detailed formatting
logging.basicConfig(
    filename='logs/app_debug.log',  # Log file location
    level=logging.DEBUG,  # Capture all levels
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'  # Custom date format
)

# Also log to console for immediate feedback
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Only INFO and above to console
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)

# Get logger and add console handler
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)

def process_user_data(user_id, data):
    """
    Process user data with comprehensive logging
    
    Demonstrates all logging levels in realistic scenarios
    """
    logger.debug(f"Processing started for user {user_id}")
    logger.debug(f"Input data: {data}")
    
    # Check if data is empty
    if not data:
        logger.warning(f"Empty data received for user {user_id}")
        logger.info(f"Skipping processing for user {user_id} due to empty data")
        return None
    
    # Check data type
    if not isinstance(data, dict):
        logger.error(f"Invalid data type for user {user_id}: expected dict, got {type(data).__name__}")
        return None
    
    try:
        # Process data
        logger.info(f"Processing user {user_id} with {len(data)} fields")
        
        processed = {}
        for key, value in data.items():
            logger.debug(f"Processing field '{key}' for user {user_id}")
            
            if not isinstance(value, str):
                logger.warning(f"Non-string value for field '{key}': {value} ({type(value).__name__})")
                processed[key] = str(value)  # Convert to string
            else:
                processed[key] = value.upper()
        
        logger.info(f"Successfully processed user {user_id}")
        logger.debug(f"Processed data: {processed}")
        return processed
        
    except AttributeError as e:
        logger.error(f"AttributeError while processing user {user_id}: {e}")
        logger.debug(f"Problematic data: {data}", exc_info=True)  # Include traceback
        return None
        
    except Exception as e:
        logger.critical(f"Unexpected critical error for user {user_id}: {e}")
        logger.debug("Full traceback:", exc_info=True)
        raise

def demonstrate_logging_levels():
    """
    Demonstrate all logging levels with different scenarios
    """
    logger.info("="*60)
    logger.info("LOGGING DEMONSTRATION STARTED")
    logger.info("="*60)
    
    # DEBUG level - detailed diagnostic
    logger.debug("Debug: Starting demonstration function")
    logger.debug(f"Debug: Current time is {datetime.now()}")
    
    # INFO level - normal operations
    logger.info("Info: Application running normally")
    
    # WARNING level - unexpected but handled
    logger.warning("Warning: This is a warning message - something unusual happened")
    
    # ERROR level - operation failed
    logger.error("Error: This is an error message - operation failed")
    
    # CRITICAL level - serious error
    logger.critical("Critical: This is a critical message - system in danger")

# Run demonstrations
print("Starting logging demonstration...")
print("Check 'logs/app_debug.log' for complete log output\n")

demonstrate_logging_levels()

print("\n" + "="*60)
print("PROCESSING USERS")
print("="*60 + "\n")

# Test Case 1: Valid data
print("Test 1: Valid user data")
result1 = process_user_data(123, {"name": "john", "city": "NYC", "role": "developer"})
print(f"Result: {result1}\n")

# Test Case 2: Empty data
print("Test 2: Empty data")
result2 = process_user_data(456, None)
print(f"Result: {result2}\n")

# Test Case 3: Invalid data type
print("Test 3: Mixed data types")
result3 = process_user_data(789, {"name": "alice", "age": 30, "active": True})
print(f"Result: {result3}\n")

# Test Case 4: Non-dict data
print("Test 4: Invalid data structure")
result4 = process_user_data(999, "not a dictionary")
print(f"Result: {result4}\n")

print("="*60)
print(f"Logging complete! Check 'logs/app_debug.log' for full details")
print("="*60)