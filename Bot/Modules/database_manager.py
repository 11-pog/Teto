import asyncio, aiosqlite
from functools import wraps
from typing import Any, Callable, Iterable, List, Mapping, Optional, Set

from resources_path import resources_path

class DatabaseManager:
    _instances: Set["DatabaseManager"] = set()
    
    def __init__(self, auto_connect: bool = True, loop: Optional[asyncio.AbstractEventLoop] = None):
        if auto_connect and loop:
            loop.create_task(self.connect())
        elif auto_connect:
            asyncio.run(self.connect())
        
        self._instances.add(self)
    
    def __del__(self):
        if hasattr(self, "database"):
            self.loop.run_until_complete(self.database.close())
        
        self._instances.discard(self)
    
    
    async def connect(self):
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        
        self.database = await aiosqlite.connect(f"{resources_path('database')}/GeneralBotData.db")
        self.cursor = await self.database.cursor()
    
    async def disconnect(self):
        if hasattr(self, "database"):
            await self.database.close()
    
    @classmethod
    async def disconnect_all(cls):
        for instance in list(cls._instances):
            await instance.disconnect()
            instance.database = None
        
        cls._instances.clear()
    
    @staticmethod
    async def _requires_connection(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(self: DatabaseManager, *args: Any, **kwargs: Any) -> Callable[..., Any]:
            if not hasattr(self, "database") or not hasattr(self, "cursor"):
                raise RuntimeError("Database did not initialize!")
            return await func(self, *args, **kwargs)
        return wrapper
    
    
    @_requires_connection
    async def execute(self, query: str, parameters: Optional[Iterable[Any]] = None):
        return await self.cursor.execute(query, parameters)
    
    TableStructure = Mapping[str, str]
    DatabaseStructure = Mapping[str, TableStructure]
    
    @_requires_connection
    async def setup(self, structure: DatabaseStructure, always_create: bool = False):
        base_query = "CREATE TABLE "
        base_query += "IF NOT EXISTS " if always_create == False else ""
        
        for table in structure:
            columns: List[str] = []
            
            for column in structure[table]:
                columns += [f"{column} {structure[table][column]}"]
            
            init_query = base_query + table + f'({', '.join(columns)})'
            await self.database.execute(init_query)
    
    @_requires_connection
    async def fetchall(self, query: str, parameters: Optional[Iterable[Any]] = None):
        cursor = await self.cursor.execute(query, parameters)
        return await cursor.fetchall()
    
    @_requires_connection
    async def fetchone(self, query: str, parameters: Optional[Iterable[Any]] = None):
        cursor = await self.cursor.execute(query, parameters)
        return await cursor.fetchone()
    
    @_requires_connection
    async def fetchmany(self, query: str, parameters: Optional[Iterable[Any]] = None, amount: Optional[int] = None):
        cursor = await self.cursor.execute(query, parameters)
        return await cursor.fetchmany(amount)
    
    @_requires_connection
    async def commit(self, query: str | None = None, parameters: Optional[Iterable[Any]] = None):
        if query is not None:
            await self.cursor.execute(query, parameters)
        await self.database.commit()




"""
async def test(db):
    await db.commit('ALTER TABLE communityNotepad RENAME COLUMN general_ID TO server_ID')
    await db.disconnect()

if __name__ == "__main__":
    db = DatabaseManager()
    asyncio.run(test(db))
"""