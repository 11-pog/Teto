import asyncio
import nextcord

from concurrent.futures import ThreadPoolExecutor

from Cogs.youtube_playback.YTDLConfig import YTDLConfig

THREAD_EXECUTOR = ThreadPoolExecutor(max_workers=9)
CONFIG = YTDLConfig()

class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        
        self.data = data
        
        self.title = data.get('title')
        self.url = ""
    
    @classmethod
    def extract(cls, extractor, url, download):
        return extractor.extract_info(url, download=download)
    
    @classmethod
    async def wait_for_extraction(cls, loop, extractor, url, download, timeout):
        return await asyncio.wait_for(
            loop.run_in_executor(THREAD_EXECUTOR , cls.extract, extractor, url, download),
            timeout=timeout
            )
    
    @classmethod
    async def stream_from_url(cls, url, *, timeout = 30, loop=None):
        loop = loop or asyncio.get_event_loop()
        
        data = await cls.wait_for_extraction(loop, CONFIG.yt_downloader, url=url, download=False, timeout=timeout)
        
        filename = data['url']
        return cls(nextcord.FFmpegPCMAudio(filename, **CONFIG.ffmpeg_format_options), data=data)
    
    @classmethod
    async def get_info_from_url(cls, url, *, timeout = 15, loop=None):
        loop = loop or asyncio.get_event_loop()
        
        info = await cls.wait_for_extraction(loop, CONFIG.yt_info_extractor, url=url, download=False, timeout=timeout)
        
        return info