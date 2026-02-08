"""
CONCEPT: Automatic REST API endpoint generation
LEARN: Building framework-like features with metaclass
"""

class Endpoint:
    """Descriptor for API endpoints"""
    def __init__(self, method, path, handler):
        self.method = method
        self.path = path
        self.handler = handler
    
    def __call__(self, *args, **kwargs):
        return self.handler(*args, **kwargs)

def route(method, path):
    """Decorator to define API routes"""
    def decorator(func):
        func._route_method = method
        func._route_path = path
        return func
    return decorator

class APIMeta(type):
    """Metaclass that builds API routing table"""
    
    def __new__(cls, name, bases, attrs):
        routes = {}
        
        # Find all route handlers
        for attr_name, attr_value in attrs.items():
            if hasattr(attr_value, '_route_method') and hasattr(attr_value, '_route_path'):
                method = attr_value._route_method
                path = attr_value._route_path
                route_key = f"{method}:{path}"
                routes[route_key] = attr_name
        
        attrs['_routes'] = routes
        
        # Add dispatch method
        def dispatch(self, method, path, **params):
            route_key = f"{method}:{path}"
            if route_key in self._routes:
                handler_name = self._routes[route_key]
                handler = getattr(self, handler_name)
                return handler(**params)
            else:
                return {"error": "Route not found", "code": 404}
        
        attrs['dispatch'] = dispatch
        
        # Add list_routes method
        def list_routes(cls):
            return list(cls._routes.keys())
        
        attrs['list_routes'] = classmethod(list_routes)
        
        return super().__new__(cls, name, bases, attrs)

class UserAPI(metaclass=APIMeta):
    def __init__(self):
        self.users = {}
        self.user_id_counter = 1
    
    @route('GET', '/users')
    def get_users(self):
        return {"users": list(self.users.values())}
    
    @route('GET', '/users/{id}')
    def get_user(self, id):
        user = self.users.get(int(id))
        if user:
            return {"user": user}
        return {"error": "User not found", "code": 404}
    
    @route('POST', '/users')
    def create_user(self, name, email):
        user_id = self.user_id_counter
        self.user_id_counter += 1
        
        user = {"id": user_id, "name": name, "email": email}
        self.users[user_id] = user
        
        return {"user": user, "code": 201}
    
    @route('PUT', '/users/{id}')
    def update_user(self, id, name=None, email=None):
        user_id = int(id)
        if user_id not in self.users:
            return {"error": "User not found", "code": 404}
        
        if name:
            self.users[user_id]['name'] = name
        if email:
            self.users[user_id]['email'] = email
        
        return {"user": self.users[user_id]}
    
    @route('DELETE', '/users/{id}')
    def delete_user(self, id):
        user_id = int(id)
        if user_id in self.users:
            del self.users[user_id]
            return {"message": "User deleted", "code": 200}
        return {"error": "User not found", "code": 404}

if __name__ == "__main__":
    api = UserAPI()
    
    print("Available routes:")
    for route in api.list_routes():
        print(f"  {route}")
    
    print("\n--- API Testing ---")
    
    # Create users
    print("\n1. Creating users:")
    print(api.dispatch('POST', '/users', name="Alice", email="alice@example.com"))
    print(api.dispatch('POST', '/users', name="Bob", email="bob@example.com"))
    
    # Get all users
    print("\n2. Getting all users:")
    print(api.dispatch('GET', '/users'))
    
    # Get specific user
    print("\n3. Getting user with id=1:")
    print(api.dispatch('GET', '/users/{id}', id=1))
    
    # Update user
    print("\n4. Updating user 1:")
    print(api.dispatch('PUT', '/users/{id}', id=1, name="Alice Smith"))
    
    # Delete user
    print("\n5. Deleting user 2:")
    print(api.dispatch('DELETE', '/users/{id}', id=2))
    
    # Final state
    print("\n6. Final user list:")
    print(api.dispatch('GET', '/users'))