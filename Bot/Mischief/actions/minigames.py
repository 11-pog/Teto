from mischief.interface import TextMischief


class MINIGAMES(TextMischief):
    mischief_name = 'minigames'
    
    def check(self, normalized_text, message):
        return 'minigames' in normalized_text
    
    async def execute(self, normalized_text, message):
        await message.add_reaction("<:MINIGAMES:1400192834073530400>")