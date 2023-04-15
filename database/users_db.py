import aiosqlite
import asyncio
import nest_asyncio

nest_asyncio.apply() # костыль

class Users:
    def __init__(self):
        self.connection : aiosqlite.Connection = None
        self.cursor : aiosqlite.Cursor = None
        asyncio.run(self.connect())

    async def connect(self):
        self.connection = await aiosqlite.connect(f'database/users.db')
        self.cursor = await self.connection.cursor()
    
    async def add_user(self, user_id, lang):
        await self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        data = await self.cursor.fetchone()

        if data is None:
            await self.cursor.execute("INSERT INTO users (user_id, lang) VALUES (?, ?)", (user_id, lang,))
            await self.connection.commit()
            return True

        await self.cursor.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id,))
        await self.connection.commit()
        return False

    async def get_language(self, user_id):
        await self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        data = await self.cursor.fetchone()
        
        if data is None:
            return None
        
        return data[2]