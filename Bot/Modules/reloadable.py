import weakref


class ReloadableComponent:
    _instances = weakref.WeakSet()
    
    def __init__(self):
        ReloadableComponent._instances.add(self)
    
    
    def load(self):
        """
        Abstract method to load necessary resources or perform initialization steps for the module.
        
        This method serves as a contract for subclasses, ensuring that any component
        inheriting from ReloadableComponent implements its own loading logic. It is
        called to initialize or set up resources required by the module.
        
        Subclasses may override this method to define specific loading behavior.
        """
        pass
    
    
    def reload(self):
        """
        Reloads the module or component.
        
        This method is intended to be overridden by subclasses to implement custom
        reload logic when the bot is reloaded. It is called automatically during
        the bot's reload process to allow for resource cleanup, reinitialization,
        or other necessary updates.
        
        Override this method to define specific behavior that should occur when
        the bot reloads this module.
        
        Raises:
            NotImplementedError: If the method is not overridden in a subclass.
        """
        raise NotImplementedError("Subclasses of ReloadableComponent must implement the reload() method.")
    
    
    @classmethod
    def reload_all_instances(cls):
        for instance in cls._instances:
            instance.reload()
