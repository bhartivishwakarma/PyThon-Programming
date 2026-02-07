"""
CONCEPT: Basic thread creation
LEARN: How to create and start threads
"""

import threading
import time

def say_hello(name, delay):
    """Function that will run in a separate thread"""
    time.sleep(delay)
    print(f"Hello from {name}! (Thread ID: {threading.current_thread().name})")

if __name__ == "__main__":
    print("Main program starting...")
    
    # Create threads
    thread1 = threading.Thread(target=say_hello, args=("Thread-1", 1))
    thread2 = threading.Thread(target=say_hello, args=("Thread-2", 2))
    thread3 = threading.Thread(target=say_hello, args=("Thread-3", 0.5))
    
    # Start threads
    print("\nStarting threads...")
    thread1.start()
    thread2.start()
    thread3.start()
    
    # Wait for all threads to complete
    thread1.join()
    thread2.join()
    thread3.join()
    
    print("\nAll threads completed!")
    print("Main program ending...")

