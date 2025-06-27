import os, json, resources_path
from discord import Enum


class SettingType(Enum):
    BOT = 0
    MISCHIEF = 1

SETTINGS_PATH = resources_path.SETTINGS


class Settings:
    def __init__(self, setting_type: SettingType):
        self.setting_type = setting_type
    
    
    @staticmethod
    def create_file(filename: str):
        path = os.path.join(SETTINGS_PATH, filename)
        
        if not os.path.exists(path):
            os.makedirs(SETTINGS_PATH, exist_ok=True) 
            
            with open(path, 'x', encoding='utf-8') as f:
                json.dump({}, f)
    
    
    @staticmethod
    def create_settings():
        for setting in SettingType:
            Settings.create_file(f"{setting.name.lower()}.json")