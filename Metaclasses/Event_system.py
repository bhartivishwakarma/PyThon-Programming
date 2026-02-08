"""
CONCEPT: Event-driven programming with metaclass
LEARN: Automatic event handler registration
"""

class EventMeta(type):
    """Metaclass for event-driven classes"""
    
    def __new__(cls, name, bases, attrs):
        # Find all event handler methods
        event_handlers = {}
        
        for attr_name, attr_value in attrs.items():
            if hasattr(attr_value, '_event_name'):
                event_name = attr_value._event_name
                if event_name not in event_handlers:
                    event_handlers[event_name] = []
                event_handlers[event_name].append(attr_name)
        
        attrs['_event_handlers'] = event_handlers
        
        # Add emit method
        def emit(self, event_name, *args, **kwargs):
            handlers = self._event_handlers.get(event_name, [])
            results = []
            for handler_name in handlers:
                handler = getattr(self, handler_name)
                result = handler(*args, **kwargs)
                results.append(result)
            return results
        
        attrs['emit'] = emit
        
        # Add list_events method
        def list_events(cls):
            return list(cls._event_handlers.keys())
        
        attrs['list_events'] = classmethod(list_events)
        
        return super().__new__(cls, name, bases, attrs)

def event_handler(event_name):
    """Decorator to mark methods as event handlers"""
    def decorator(func):
        func._event_name = event_name
        return func
    return decorator

class UserSystem(metaclass=EventMeta):
    def __init__(self):
        self.users = []
    
    @event_handler('user_created')
    def send_welcome_email(self, username):
        return f"Welcome email sent to {username}"
    
    @event_handler('user_created')
    def create_user_folder(self, username):
        return f"Folder created for {username}"
    
    @event_handler('user_created')
    def log_user_creation(self, username):
        return f"Logged: User {username} created"
    
    @event_handler('user_deleted')
    def remove_user_data(self, username):
        return f"Data removed for {username}"
    
    @event_handler('user_deleted')
    def log_user_deletion(self, username):
        return f"Logged: User {username} deleted"
    
    def create_user(self, username):
        self.users.append(username)
        results = self.emit('user_created', username)
        return results
    
    def delete_user(self, username):
        if username in self.users:
            self.users.remove(username)
        results = self.emit('user_deleted', username)
        return results

if __name__ == "__main__":
    system = UserSystem()
    
    print("Available events:", system.list_events())
    
    print("\nCreating user 'Alice':")
    results = system.create_user("Alice")
    for result in results:
        print(f"  - {result}")
    
    print("\nDeleting user 'Alice':")
    results = system.delete_user("Alice")
    for result in results:
        print(f"  - {result}")