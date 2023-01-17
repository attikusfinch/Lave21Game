import aiosqlite

class WithdrawHistory:
    async def set_withdraw(self, user_id: int, withdraw_address: str, amount: int):
        async with aiosqlite.connect('database/withdraw.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("INSERT INTO withdraw_history (user_id, withdraw_address, amount) VALUES (?, ?, ?)", (user_id, withdraw_address, amount,))
                await connection.commit()
                return True

    async def get_withdraw_address(self, user_id: int):
        async with aiosqlite.connect('database/withdraw.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT withdraw_address FROM withdraw_history WHERE user_id = ?", (user_id,))
                
                withdraw_address = await cursor.fetchone()
                
                if withdraw_address is None:
                    return None
                
                return withdraw_address

    async def get_all_addresses(self):
        async with aiosqlite.connect('database/withdraw.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM withdraw_history")
                
                withdraw_address = await cursor.fetchall()
                
                if len(withdraw_address) == 0:
                    return []
                
                return withdraw_address

    async def get_user(self, withdraw_address: str):
        async with aiosqlite.connect('database/withdraw.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT user_id FROM withdraw_history WHERE withdraw_address = ?", (withdraw_address,))
                
                user_id = await cursor.fetchone()
                
                if user_id is None:
                    return None
                
                return user_id

    async def delete_withdraw(self, user_id):
        async with aiosqlite.connect('database/withdraw.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("DELETE FROM withdraw_history WHERE user_id = ?", (user_id,))
                await connection.commit()
                return True