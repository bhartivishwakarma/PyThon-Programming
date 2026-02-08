"""
CONCEPT: Implementing Singleton pattern
LEARN: Control instance creation with metaclass
"""

class SingletonMeta(type):
    """Metaclass that creates a Singleton"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        print(f"Connecting to database: {connection_string}")
    
    def query(self, sql):
        return f"Executing: {sql}"

class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.logs = []
        print("Logger initialized")
    
    def log(self, message):
        self.logs.append(message)
        print(f"LOG: {message}")

if __name__ == "__main__":
    # Creating database instances
    db1 = Database("localhost:5432")
    db2 = Database("different_host:3306")  # Same instance!
    
    print(f"\ndb1 is db2: {db1 is db2}")
    print(f"db1 connection: {db1.connection_string}")
    print(f"db2 connection: {db2.connection_string}")
    
    # Logger instances
    logger1 = Logger()
    logger2 = Logger()
    
    logger1.log("First message")
    logger2.log("Second message")
    
    print(f"\nlogger1 is logger2: {logger1 is logger2}")
    print(f"Total logs: {len(logger1.logs)}")