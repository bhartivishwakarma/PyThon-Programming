"""
CONCEPT: Using locks to protect shared data
LEARN: How to prevent race conditions
"""

import threading
import time
import random

class BankAccount:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.lock = threading.Lock()  # Create a lock
    
    def deposit(self, amount, name):
        """Safely deposit money"""
        with self.lock:  # Acquire lock automatically
            print(f"{name}: Depositing ${amount}")
            current_balance = self.balance
            time.sleep(0.1)  # Simulate processing
            self.balance = current_balance + amount
            print(f"{name}: New balance ${self.balance}")
    
    def withdraw(self, amount, name):
        """Safely withdraw money"""
        with self.lock:  # Acquire lock automatically
            print(f"{name}: Withdrawing ${amount}")
            if self.balance >= amount:
                current_balance = self.balance
                time.sleep(0.1)  # Simulate processing
                self.balance = current_balance - amount
                print(f"{name}: New balance ${self.balance}")
            else:
                print(f"{name}: Insufficient funds!")
    
    def get_balance(self):
        """Get current balance"""
        with self.lock:
            return self.balance

def do_transactions(account, person_name, num_transactions):
    """Perform random deposits and withdrawals"""
    for i in range(num_transactions):
        if random.choice([True, False]):
            amount = random.randint(10, 100)
            account.deposit(amount, person_name)
        else:
            amount = random.randint(10, 100)
            account.withdraw(amount, person_name)
        time.sleep(0.2)

if __name__ == "__main__":
    print("=== SAFE BANK ACCOUNT WITH LOCKS ===\n")
    
    # Create account with $1000
    account = BankAccount(1000)
    print(f"Initial balance: ${account.get_balance()}\n")
    
    # Create threads for two people
    person1 = threading.Thread(
        target=do_transactions, 
        args=(account, "Alice", 5)
    )
    person2 = threading.Thread(
        target=do_transactions, 
        args=(account, "Bob", 5)
    )
    
    # Start transactions
    person1.start()
    person2.start()
    
    # Wait for completion
    person1.join()
    person2.join()
    
    print(f"\n✓ Final balance: ${account.get_balance()}")
    print("✓ No race conditions - all transactions safe!")

"""
OUTPUT:
=== SAFE BANK ACCOUNT WITH LOCKS ===

Initial balance: $1000

Alice: Depositing $45
Alice: New balance $1045
Bob: Withdrawing $67
Bob: New balance $978
Alice: Depositing $23
Alice: New balance $1001
...

✓ Final balance: $1023
✓ No race conditions - all transactions safe!

KEY CONCEPTS:
✓ threading.Lock() - creates a lock object
✓ with lock: - automatically acquires and releases
✓ Only one thread can hold the lock at a time
"""