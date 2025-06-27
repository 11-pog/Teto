import asyncio, aiosqlite, resources_path
from functools import wraps
from typing import Any, Callable, Iterable, List, Mapping, Optional, Set

class DatabaseManager:
    database = None
    cursor = None
    
    def __init__(self):
        pass
    
    @classmethod
    async def connect(cls):
        cls.database = await aiosqlite.connect(f"{resources_path.DATABASES}/GeneralBotData.db")
        cls.cursor = await cls.database.cursor()
    
    @classmethod
    async def disconnect(cls):
        if cls.database is not None:
            await cls.database.close()
    
    @staticmethod
    def _requires_connection(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
            if DatabaseManager.database is None or DatabaseManager.cursor is None:
                raise RuntimeError("Database did not initialize!")
            return await func(self, *args, **kwargs)
        return wrapper
    
    
    @_requires_connection
    async def execute(self, query: str, parameters: Optional[Iterable[Any]] = None):
        return await DatabaseManager.cursor.execute(query, parameters)
    
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
            await DatabaseManager.database.execute(init_query)
    
    @_requires_connection
    async def fetchall(self, query: str, parameters: Optional[Iterable[Any]] = None):
        cursor = await DatabaseManager.cursor.execute(query, parameters)
        return await cursor.fetchall()
    
    @_requires_connection
    async def fetchone(self, query: str, parameters: Optional[Iterable[Any]] = None):
        cursor = await DatabaseManager.cursor.execute(query, parameters)
        return await cursor.fetchone()
    
    @_requires_connection
    async def fetchmany(self, query: str, parameters: Optional[Iterable[Any]] = None, amount: Optional[int] = None):
        cursor = await DatabaseManager.cursor.execute(query, parameters)
        return await cursor.fetchmany(amount)
    
    @_requires_connection
    async def commit(self, query: str | None = None, parameters: Optional[Iterable[Any]] = None):
        if query is not None:
            await DatabaseManager.cursor.execute(query, parameters)
        await DatabaseManager.database.commit()




"""
async def test(db):
    await db.commit('ALTER TABLE communityNotepad RENAME COLUMN general_ID TO server_ID')
    await db.disconnect()

if __name__ == "__main__":
    db = DatabaseManager()
    asyncio.run(test(db))
"""