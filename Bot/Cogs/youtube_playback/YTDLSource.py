import asyncio
import nextcord

from Cogs.youtube_playback.YTDLConfig import YTDLConfig

class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def stream_from_url(cls, url, *, timeout = 30, config: YTDLConfig, loop=None):
        loop = loop or asyncio.get_event_loop()

        data = await asyncio.wait_for(loop.run_in_executor(None, lambda: config.yt_downloader.extract_info(url, download=False)), timeout=timeout)

        filename = data['url']
        return cls(nextcord.FFmpegPCMAudio(filename, **config.ffmpeg_format_options), data=data)
        
    @classmethod
    async def get_info_from_url(cls, url, *, timeout = 15, config: YTDLConfig, loop=None):
        loop = loop or asyncio.get_event_loop()
        info = await asyncio.wait_for(loop.run_in_executor(None, lambda: config.yt_info_extractor.extract_info(url, download=False)), timeout=timeout)

        return info