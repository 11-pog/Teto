import os, json, resources_path
from typing import Any, Dict, List


SETTINGS_PATH = resources_path.SETTINGS

class Settings(dict):
    _instances: List["Settings"] = []
    
    def __init__(self, name: str):
        self.name = name
        self.path = self.get_path()
        
        super().__init__()
        
        if not os.path.exists(self.path):
            self.create_file()
        else:
            self.load()
        
        Settings._instances.append(self)
    
    
    @classmethod
    def reload(cls):
        for instance in cls._instances:
            instance.load()
    
    
    def get_path(self) -> str:
        filename = f"{self.name.lower()}.json"
        return os.path.join(SETTINGS_PATH, filename)
    
    
    def create_file(self):
        os.makedirs(SETTINGS_PATH, exist_ok=True) 
        with open(self.path, 'x', encoding='utf-8') as f:
            json.dump({}, f)
    
    
    def save(self):
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(self, f, indent=4, ensure_ascii=True)
    
    def load(self):
        with open(self.path, "r", encoding='utf-8') as f:
            data = json.load(f)
            self.clear()
            self.update(data)
    
    
    def setup(self, default_structure = Dict[str, Any]):
        self.load()
        
        for key in default_structure:
            if key not in self:
                self[key] = default_structure[key]
        
        self.save()