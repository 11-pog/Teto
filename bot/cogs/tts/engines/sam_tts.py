import asyncio
from io import BytesIO
import discord
from samtts import SamTTS
from cogs.tts.abc import TTSEngineBase

from modules.logging.logger import logger

class SamTTSEngine(TTSEngineBase):
    engine_name = "samtts"
    engine_description = "FV1 RFORM FUCKING UTLRKAIKILL LEJKST GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    
    default_lang = 'sam'
    
    SAM_languages = {
        'elf': (72, 64, 160, 110),
        'robot': (92, 60, 190, 190),
        'guy': (82, 72, 105, 110),
        'old-lady': (82, 32, 145, 145),
        'alien': (100, 64, 200, 150),
        'sam': (72, 64, 128, 128),
    }
    special_language_codes = { # TODO: Implement this
        "custom": "[s] [p] [m] [t]"
        }
    
    SAM_language_codes = {
        'elf': 'Elf',
        'robot': 'Little Robot',
        'guy': 'Stuffy Guy',
        'old-lady': 'Little Old Lady',
        'alien': 'Extra-Terrestrial',
        'sam': 'SAM',
        'custom [speed] [pitch] [mouth] [throat]': 'Custom Settings [NOT IMPLEMENTED]'
    }
    
    @classmethod
    def get_languages(cls):
        return cls.SAM_language_codes
    
    async def get_audio_source(self):
        buffer = BytesIO()
        
        speed, pitch, mouth, throat = self.SAM_languages.get(self.language, (72, 64, 128, 128))
        
        def run_sam():
            def get_audio_as_bytearray(
                audio_data: bytes | bytearray,
                num_channels: int = 1,
                bytes_per_sample: int = 1,
                sample_rate: int = 22050,
            ):
                buffer.write(audio_data)
            
            SamTTS(
                speed=speed,
                pitch=pitch,
                mouth=mouth,
                throat=throat,
                ).play(
                self.text,
                play_audio_data = get_audio_as_bytearray,
            )
        
        await asyncio.wait_for(
            asyncio.to_thread(run_sam),
            timeout=5
        )
        
        await asyncio.sleep(1)
        
        buffer.seek(0)
        audio_source = discord.FFmpegPCMAudio(
            buffer,
            pipe=True,
            before_options=(
                "-f u8 "
                "-ar 22050 "
                "-ac 1"
            ),
            options="-f s16le -ar 48000 -ac 2 -filter:a volume=0.4"
        )
        
        return audio_source
