import aiosqlite

class Wallet:
    async def add_wallet(self, user_id, lave_count=0, ton_count=0, withdraw_address=None):
        async with aiosqlite.connect('database/wallet.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM wallet WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()

                if data is None:
                    await cursor.execute("INSERT INTO wallet (user_id, lave_count, ton_count, withdraw_address) VALUES (?, ?, ?, ?)", (user_id, lave_count, ton_count, withdraw_address))
                    await connection.commit()
                    return True

                return False

    async def get_wallet(self, user_id):
        async with aiosqlite.connect('database/wallet.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM wallet WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()
                
                if data is None:
                    return None
                
                return data[4]
            
    async def set_wallet(self, user_id, withdraw_address):
        async with aiosqlite.connect('database/wallet.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM wallet WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()

                if data is None:
                    return None

                await cursor.execute("UPDATE wallet SET withdraw_address = ? WHERE user_id = ?", (withdraw_address, user_id))
                await connection.commit()
                return True


    async def get_lave(self, user_id):
        async with aiosqlite.connect('database/wallet.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT lave_count FROM wallet WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()
                
                if data is None:
                    return None
                
                return data[0]

    async def set_lave(self, user_id, amount, add=True):
        async with aiosqlite.connect('database/wallet.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT lave_count FROM wallet WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()
                
                if data is None:
                    return None
                
                symbol = "+" if add else "-"

                await cursor.execute(f"UPDATE wallet SET lave_count = lave_count {symbol} ? WHERE user_id = ?", (amount, user_id,))
                await connection.commit()

                return True

    async def get_ton(self, user_id):
        async with aiosqlite.connect('database/wallet.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT ton_count FROM wallet WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()
                
                if data is None:
                    return None
                
                return data[0]

    async def set_ton(self, user_id, amount, add=True):
        async with aiosqlite.connect('database/wallet.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT ton_count FROM wallet WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()
                
                if data is None:
                    return None
                
                symbol = "+" if add else "-"
                
                await cursor.execute(f"UPDATE wallet SET ton_count = ton_count {symbol} ? WHERE user_id = ?", (amount, user_id,))
                await connection.commit()
                
                return True