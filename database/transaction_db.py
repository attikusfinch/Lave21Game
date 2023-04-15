import aiosqlite
import asyncio

class Transactions:
    def __init__(self):
        self.connection : aiosqlite.Connection = None
        self.cursor : aiosqlite.Cursor = None
        asyncio.run(self.connect())

    async def connect(self):
        self.connection = await aiosqlite.connect(f'database/transactions.db')
        self.cursor = await self.connection.cursor()
    
    async def add_transaction(self, jetton_date, jetton_comment):
        await self.cursor.execute("INSERT INTO transaction_history (jetton_date, jetton_comment) VALUES (?, ?)", (jetton_date, jetton_comment,))
        await self.connection.commit()

    async def check_transaction(self, jetton_date, jetton_comment):
        """
        Check if transaction is exist
        """
        await self.cursor.execute("SELECT * FROM transaction_history WHERE jetton_date = ? AND jetton_comment = ?", (jetton_date, jetton_comment,))
        data = await self.cursor.fetchone()
        
        if data is None:
            return False
        
        return True