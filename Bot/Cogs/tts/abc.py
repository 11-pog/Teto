from abc import ABC, abstractmethod
from io import BytesIO
from typing import List


class TTSEngineBase(ABC):
    engine_name: str = ...
    
    def_lang: str = ...
    special_language_codes: List[str] = []
    
    text: str = ...
    language: str = ...
    
    def __init__(self, text, lang):
        text, language = self.get_user_language(text, lang) # TODO: treatment for special language codes
        
        if not self.language_exists(language):
            language = lang
        
        self.language = language
        self.text = text
    
    @abstractmethod
    async def get_audio_source(self, text: str) -> BytesIO: ...
    
    @classmethod
    @abstractmethod
    def get_languages(cls) -> dict: ...
    
    @classmethod
    def language_exists(cls, lang_code: str) -> bool:
        available = cls.get_languages()
        return lang_code in available.keys()
    
    def get_user_language(self, text, default):
        keyword_list = text.split(' ')
        
        for word in keyword_list:
            if word.startswith("--lang:"):
                lang = word.removeprefix('--lang:').strip()
                text = text.replace(word, "")
                return text, lang
        
        return text, default