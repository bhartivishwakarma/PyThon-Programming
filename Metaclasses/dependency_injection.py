"""
CONCEPT: Automatic dependency injection container
LEARN: IoC (Inversion of Control) pattern with metaclass
"""

import inspect
from typing import get_type_hints

class DependencyContainer:
    """Container for managing dependencies"""
    def __init__(self):
        self._services = {}
        self._singletons = {}
    
    def register(self, service_type, implementation=None, singleton=False):
        """Register a service"""
        if implementation is None:
            implementation = service_type
        
        self._services[service_type] = {
            'implementation': implementation,
            'singleton': singleton
        }
    
    def resolve(self, service_type):
        """Resolve a service instance"""
        if service_type not in self._services:
            raise ValueError(f"Service {service_type.__name__} not registered")
        
        service_info = self._services[service_type]
        implementation = service_info['implementation']
        
        # Return singleton if exists
        if service_info['singleton'] and service_type in self._singletons:
            return self._singletons[service_type]
        
        # Create instance with dependency injection
        instance = self._create_instance(implementation)
        
        # Store singleton
        if service_info['singleton']:
            self._singletons[service_type] = instance
        
        return instance
    
    def _create_instance(self, cls):
        """Create instance with automatic dependency injection"""
        sig = inspect.signature(cls.__init__)
        dependencies = {}
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            
            # Get type annotation
            if param.annotation != inspect.Parameter.empty:
                param_type = param.annotation
                dependencies[param_name] = self.resolve(param_type)
        
        return cls(**dependencies)

class InjectableMeta(type):
    """Metaclass for dependency injection"""
    _container = DependencyContainer()
    
    def __new__(cls, name, bases, attrs):
        # Mark class as injectable
        attrs['_injectable'] = True
        
        # Store original __init__
        original_init = attrs.get('__init__')
        
        # Create new __init__ with dependency injection
        def new_init(self, **kwargs):
            # Get type hints for dependencies
            if original_init:
                sig = inspect.signature(original_init)
                injected_kwargs = {}
                
                for param_name, param in sig.parameters.items():
                    if param_name == 'self':
                        continue
                    
                    # If not provided and has type annotation, inject it
                    if param_name not in kwargs and param.annotation != inspect.Parameter.empty:
                        try:
                            injected_kwargs[param_name] = cls._container.resolve(param.annotation)
                        except ValueError:
                            # Not registered, skip
                            pass
                
                # Merge provided and injected kwargs
                final_kwargs = {**injected_kwargs, **kwargs}
                original_init(self, **final_kwargs)
        
        if original_init:
            attrs['__init__'] = new_init
        
        new_class = super().__new__(cls, name, bases, attrs)
        
        # Add class method to access container
        @classmethod
        def get_container(cls):
            return InjectableMeta._container
        
        new_class.get_container = get_container
        
        return new_class

# Service interfaces and implementations
class ILogger(metaclass=InjectableMeta):
    def log(self, message):
        raise NotImplementedError

class ConsoleLogger(ILogger):
    def log(self, message):
        print(f"[LOG] {message}")

class IDatabase(metaclass=InjectableMeta):
    def query(self, sql):
        raise NotImplementedError

class MockDatabase(IDatabase):
    def __init__(self):
        self.queries = []
    
    def query(self, sql):
        self.queries.append(sql)
        return f"Executed: {sql}"

class IEmailService(metaclass=InjectableMeta):
    def send(self, to, subject, body):
        raise NotImplementedError

class EmailService(IEmailService):
    def __init__(self, logger: ILogger):
        self.logger = logger
    
    def send(self, to, subject, body):
        self.logger.log(f"Sending email to {to}: {subject}")
        return f"Email sent to {to}"

class UserRepository(metaclass=InjectableMeta):
    def __init__(self, database: IDatabase, logger: ILogger):
        self.database = database
        self.logger = logger
    
    def create_user(self, username, email):
        self.logger.log(f"Creating user: {username}")
        result = self.database.query(f"INSERT INTO users VALUES ('{username}', '{email}')")
        return result
    
    def get_user(self, username):
        self.logger.log(f"Getting user: {username}")
        result = self.database.query(f"SELECT * FROM users WHERE username='{username}'")
        return result

class UserService(metaclass=InjectableMeta):
    def __init__(self, repository: UserRepository, email_service: IEmailService):
        self.repository = repository
        self.email_service = email_service
    
    def register_user(self, username, email):
        self.repository.create_user(username, email)
        self.email_service.send(email, "Welcome!", f"Welcome {username}!")
        return f"User {username} registered successfully"

if __name__ == "__main__":
    # Get container
    container = InjectableMeta._container
    
    # Register services
    print("Registering services...")
    container.register(ILogger, ConsoleLogger, singleton=True)
    container.register(IDatabase, MockDatabase, singleton=True)
    container.register(IEmailService, EmailService)
    container.register(UserRepository)
    container.register(UserService)
    
    print("\n--- Creating UserService (with auto dependency injection) ---")
    user_service = container.resolve(UserService)
    
    print("\n--- Using UserService ---")
    result = user_service.register_user("alice", "alice@example.com")
    print(f"Result: {result}")
    
    print("\n--- Registering another user ---")
    result = user_service.register_user("bob", "bob@example.com")
    print(f"Result: {result}")
    
    print("\n--- Checking singleton behavior ---")
    logger1 = container.resolve(ILogger)
    logger2 = container.resolve(ILogger)
    print(f"Logger is singleton: {logger1 is logger2}")
    
    email1 = container.resolve(IEmailService)
    email2 = container.resolve(IEmailService)
    print(f"EmailService is singleton: {email1 is email2}")