import aiosqlite
import asyncio

class WithdrawHistory:
    def __init__(self):
        self.connection : aiosqlite.Connection = None
        self.cursor : aiosqlite.Cursor = None
        asyncio.run(self.connect())

    async def connect(self):
        self.connection = await aiosqlite.connect(f'database/wallet.db')
        self.cursor = await self.connection.cursor()
        
    async def set_withdraw(self, user_id: int, withdraw_address: str, amount: int):
        await self.cursor.execute("INSERT INTO withdraw_history (user_id, withdraw_address, amount) VALUES (?, ?, ?)", (user_id, withdraw_address, amount,))
        await self.connection.commit()
        return True

    async def get_withdraw_address(self, user_id: int):
        await self.cursor.execute("SELECT withdraw_address FROM withdraw_history WHERE user_id = ?", (user_id,))
        
        withdraw_address = await self.cursor.fetchone()
        
        if withdraw_address is None:
            return None
        
        return withdraw_address

    async def get_all_addresses(self):
        await self.cursor.execute("SELECT * FROM withdraw_history")
        
        withdraw_address = await self.cursor.fetchall()
        
        if len(withdraw_address) == 0:
            return []
        
        return withdraw_address

    async def get_user(self, withdraw_address: str):
        await self.cursor.execute("SELECT user_id FROM withdraw_history WHERE withdraw_address = ?", (withdraw_address,))
        
        user_id = await self.cursor.fetchone()
        
        if user_id is None:
            return None
        
        return user_id

    async def delete_withdraw(self, user_id):
        await self.cursor.execute("DELETE FROM withdraw_history WHERE user_id = ?", (user_id,))
        await self.connection.commit()
        return True