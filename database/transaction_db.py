import aiosqlite

class Transactions:
    async def add_transaction(self, jetton_date, jetton_comment):
        async with aiosqlite.connect('database/transactions.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("INSERT INTO transaction_history (jetton_date, jetton_comment) VALUES (?, ?)", (jetton_date, jetton_comment,))
                await connection.commit()

    async def check_transaction(self, jetton_date, jetton_comment):
        """
        Check if transaction is exist
        """
        async with aiosqlite.connect('database/transactions.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM transaction_history WHERE jetton_date = ? AND jetton_comment = ?", (jetton_date, jetton_comment,))
                data = await cursor.fetchone()
                
                if data is None:
                    return False
                
                return True