from io import BytesIO

import discord
from Cogs.tts.abc import TTSEngineBase
from gtts import gTTS
from gtts.lang import tts_langs


class GoogleTTSEngine(TTSEngineBase):
    engine_name = "google"
    engine_description = "Google's text to speech Y'know"
    
    default_lang = "es"
    
    def __init__(self, text, lang):
        super().__init__(text, lang)
        
        self.gtts = gTTS(text=self.text, lang=self.language, slow=False)
    
    async def get_audio_source(self):
        audio_buffer = BytesIO()
        self.gtts.write_to_fp(audio_buffer)
        
        audio_buffer.seek(0)
        audio_source = discord.FFmpegPCMAudio(audio_buffer, pipe=True, before_options='-re')
        
        return audio_source
    
    @classmethod
    def get_languages(cls):
        available = tts_langs()
        return available