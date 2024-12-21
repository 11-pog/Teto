import asyncio
import aiosqlite
from resources_path import ResourcesPath

# TODO: maybe implement modularity instead of hard-coding, i dont know
class DatabaseManager:
    def __init__(self, *, initialize = True):
        self.resources = ResourcesPath()
        
        self.database = None
        self.cursor = None
        
        asyncio.run(self.connect())
        
        if initialize:
            asyncio.run(self.setup())
    
    async def connect(self):
        self.database = await aiosqlite.connect(f"{self.resources('database')}/GeneralBotData.db")
        self.cursor = await self.database.cursor()

    async def setup(self):
        await self.database.execute("CREATE TABLE IF NOT EXISTS storedLocations(channel INT, server INT, general_ID)")
        await self.database.execute("CREATE TABLE IF NOT EXISTS communityNotepad(message STR, author_ID INT, server_ID INT)")


    async def execute(self, query, parameters = None):
        return await self.cursor.execute(query, parameters)


    async def fetchall(self, query, parameters = None):
        cursor = await self.execute(query, parameters)
        return await cursor.fetchall()


    async def fetchone(self, query, parameters = None):
        cursor = await self.execute(query, parameters)
        return await cursor.fetchone()


    async def fetchmany(self, query, parameters = None, size = None):
        cursor = await self.execute(query, parameters)
        return await cursor.fetchmany(size)


    async def commit(self, query = None, parameters = None):
        if query is not None:
            await self.execute(query, parameters)
        await self.database.commit()