from typing import Protocol

# interface
class Enableable:
    is_enable: bool = True
    
    async def initiate(self) -> None:
        """Initiates the objects function, whatever it does
        """
        self.is_enable = True
    def enable(self) -> None:
        """Enables the object
        """
        ...
    def disable(self) -> None: 
        """Disables the object
        """
        ...