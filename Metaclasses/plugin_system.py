"""
CONCEPT: Auto-registering plugin system
LEARN: Automatic plugin discovery and registration
"""

class PluginMeta(type):
    """Metaclass that auto-registers plugins"""
    plugins = {}
    
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        
        # Don't register the base Plugin class itself
        if name != 'Plugin':
            plugin_name = attrs.get('plugin_name', name)
            cls.plugins[plugin_name] = new_class
            print(f"Registered plugin: {plugin_name}")
        
        return new_class
    
    @classmethod
    def get_plugin(cls, name):
        """Get a plugin by name"""
        return cls.plugins.get(name)
    
    @classmethod
    def list_plugins(cls):
        """List all registered plugins"""
        return list(cls.plugins.keys())

class Plugin(metaclass=PluginMeta):
    """Base plugin class"""
    plugin_name = None
    
    def execute(self):
        raise NotImplementedError("Plugins must implement execute()")

# Plugins are automatically registered when defined
class EmailPlugin(Plugin):
    plugin_name = "email"
    
    def execute(self):
        return "Sending email..."

class SMSPlugin(Plugin):
    plugin_name = "sms"
    
    def execute(self):
        return "Sending SMS..."

class LogPlugin(Plugin):
    plugin_name = "logger"
    
    def execute(self):
        return "Logging message..."

class PushNotificationPlugin(Plugin):
    plugin_name = "push"
    
    def execute(self):
        return "Sending push notification..."

if __name__ == "__main__":
    print(f"\nAvailable plugins: {PluginMeta.list_plugins()}")
    
    # Use plugins dynamically
    for plugin_name in PluginMeta.list_plugins():
        plugin_class = PluginMeta.get_plugin(plugin_name)
        plugin = plugin_class()
        print(f"{plugin_name}: {plugin.execute()}")
    
    # Get specific plugin
    email_plugin = PluginMeta.get_plugin('email')()
    print(f"\nDirect call: {email_plugin.execute()}")