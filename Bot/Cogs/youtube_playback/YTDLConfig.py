import yt_dlp


class YTDLConfig:
    """Configuration class for YTDLSource
    """
    def __init__(self):
        self.ytdl_format_options = {
            'format': 'bestaudio/best',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'fragment_retries': 5,
            'extract_flat': True
        }

        self.ytdl_extractor_options = {
            'extract_flat': True,
            'quiet': True,
            'noplaylist': False
        }

        self.ffmpeg_format_options = {
            'options': '-vn',
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        }

        self.yt_downloader = yt_dlp.YoutubeDL(self.ytdl_format_options)
        self.yt_info_extractor = yt_dlp.YoutubeDL(self.ytdl_extractor_options)

