"""
CONCEPT: Automatic serialization/deserialization
LEARN: JSON conversion with type preservation
"""

import json
from datetime import datetime
from typing import get_type_hints

class SerializableMeta(type):
    """Metaclass for automatic JSON serialization"""
    
    def __new__(cls, name, bases, attrs):
        # Add to_json method
        def to_json(self):
            data = {'__class__': self.__class__.__name__}
            
            for key, value in self.__dict__.items():
                if isinstance(value, datetime):
                    data[key] = {'__type__': 'datetime', 'value': value.isoformat()}
                elif hasattr(value, 'to_json'):
                    data[key] = value.to_json()
                else:
                    data[key] = value
            
            return data
        
        # Add from_json class method
        @classmethod
        def from_json(cls, data):
            if '__class__' in data:
                class_name = data.pop('__class__')
            
            instance = cls.__new__(cls)
            
            for key, value in data.items():
                if isinstance(value, dict) and '__type__' in value:
                    if value['__type__'] == 'datetime':
                        setattr(instance, key, datetime.fromisoformat(value['value']))
                else:
                    setattr(instance, key, value)
            
            return instance
        
        # Add save method
        def save(self, filename):
            with open(filename, 'w') as f:
                json.dump(self.to_json(), f, indent=2)
        
        # Add load class method
        @classmethod
        def load(cls, filename):
            with open(filename, 'r') as f:
                data = json.load(f)
            return cls.from_json(data)
        
        attrs['to_json'] = to_json
        attrs['from_json'] = from_json
        attrs['save'] = save
        attrs['load'] = load
        
        return super().__new__(cls, name, bases, attrs)

class User(metaclass=SerializableMeta):
    def __init__(self, username, email, created_at=None):
        self.username = username
        self.email = email
        self.created_at = created_at or datetime.now()
    
    def __repr__(self):
        return f"User(username='{self.username}', email='{self.email}', created_at={self.created_at})"

class BlogPost(metaclass=SerializableMeta):
    def __init__(self, title, content, author, published_at=None):
        self.title = title
        self.content = content
        self.author = author  # Can be a User instance
        self.published_at = published_at or datetime.now()
    
    def __repr__(self):
        return f"BlogPost(title='{self.title}', author={self.author})"

if __name__ == "__main__":
    # Create user
    user = User("alice", "alice@example.com")
    print(f"Original user: {user}")
    
    # Convert to JSON
    user_json = user.to_json()
    print(f"\nJSON representation:\n{json.dumps(user_json, indent=2)}")
    
    # Restore from JSON
    restored_user = User.from_json(user_json)
    print(f"\nRestored user: {restored_user}")
    
    # Save to file
    user.save('user.json')
    print("\nSaved to user.json")
    
    # Load from file
    loaded_user = User.load('user.json')
    print(f"Loaded user: {loaded_user}")
    
    # Complex example with nested object
    post = BlogPost(
        "My First Post",
        "This is the content of my first blog post.",
        user
    )
    print(f"\nBlog post: {post}")
    
    post_json = post.to_json()
    print(f"\nPost JSON:\n{json.dumps(post_json, indent=2)}")