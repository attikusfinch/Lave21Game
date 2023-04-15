import aiosqlite
import asyncio

class Wallet:
    def __init__(self):
        self.connection : aiosqlite.Connection = None
        self.cursor : aiosqlite.Cursor = None
        asyncio.run(self.connect())

    async def connect(self):
        self.connection = await aiosqlite.connect(f'database/wallet.db')
        self.cursor = await self.connection.cursor()
        
    async def add_wallet(self, user_id, lave_count=0, ton_count=0, withdraw_address=None):
        await self.cursor.execute("SELECT * FROM wallet WHERE user_id = ?", (user_id,))
        data = await self.cursor.fetchone()

        if data is None:
            await self.cursor.execute("INSERT INTO wallet (user_id, lave_count, ton_count, withdraw_address) VALUES (?, ?, ?, ?)", (user_id, lave_count, ton_count, withdraw_address))
            await self.connection.commit()
            return True

        return False

    async def get_wallet(self, user_id):
        await self.cursor.execute("SELECT * FROM wallet WHERE user_id = ?", (user_id,))
        data = await self.cursor.fetchone()
        
        if data is None:
            return None
        
        return data[4]
            
    async def set_wallet(self, user_id, withdraw_address):
        await self.cursor.execute("SELECT * FROM wallet WHERE user_id = ?", (user_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        await self.cursor.execute("UPDATE wallet SET withdraw_address = ? WHERE user_id = ?", (withdraw_address, user_id))
        await self.connection.commit()
        return True


    async def get_lave(self, user_id):
        await self.cursor.execute("SELECT lave_count FROM wallet WHERE user_id = ?", (user_id,))
        data = await self.cursor.fetchone()
        
        if data is None:
            return None
        
        return data[0]

    async def set_lave(self, user_id, amount, add=True):
        await self.cursor.execute("SELECT lave_count FROM wallet WHERE user_id = ?", (user_id,))
        data = await self.cursor.fetchone()
        
        if data is None:
            return None
        
        symbol = "+" if add else "-"

        await self.cursor.execute(f"UPDATE wallet SET lave_count = lave_count {symbol} ? WHERE user_id = ?", (amount, user_id,))
        await self.connection.commit()

        return True

    async def get_ton(self, user_id):
        await self.cursor.execute("SELECT ton_count FROM wallet WHERE user_id = ?", (user_id,))
        data = await self.cursor.fetchone()
        
        if data is None:
            return None
        
        return data[0]

    async def set_ton(self, user_id, amount, add=True):
        await self.cursor.execute("SELECT ton_count FROM wallet WHERE user_id = ?", (user_id,))
        data = await self.cursor.fetchone()
        
        if data is None:
            return None
        
        symbol = "+" if add else "-"
        
        await self.cursor.execute(f"UPDATE wallet SET ton_count = ton_count {symbol} ? WHERE user_id = ?", (amount, user_id,))
        await self.connection.commit()
        
        return True