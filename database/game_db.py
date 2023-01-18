import aiosqlite

class Game:
    async def add_game(self, bet, bank_id, game_type):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("INSERT INTO game (game_type, bet, banking, bank_id, player_id, bank_step, player_step, bank_score, player_score) VALUES (?, ?, ?, ?, ?, 0, 0, 0, 0)", (game_type, bet, False, bank_id, None))
                await connection.commit()
                return True

    async def get_game(self, game_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM game WHERE id = ?", (game_id,))
                data = await cursor.fetchone()

                if data is None:
                    return None

                return data

    async def get_game_type(self, game_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT game_type FROM game WHERE id = ?", (game_id,))
                data = await cursor.fetchone()

                if data is None:
                    return None

                return data[0]

    async def get_bank_id(self, game_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT bank_id FROM game WHERE id = ?", (game_id,))
                data = await cursor.fetchone()

                if data is None:
                    return None

                return data[0]

    async def get_player_id(self, game_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT player_id FROM game WHERE id = ?", (game_id,))
                data = await cursor.fetchone()

                if data is None:
                    return None

                return data[0]

    async def check_game(self, game_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM game WHERE id = ? AND player_id is NULL", (game_id,))
                data = await cursor.fetchone()

                if data is None:
                    return False

                return True

    async def get_user_games(self, user_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM game WHERE bank_id = ? AND player_id is NULL", (user_id,))
                data = await cursor.fetchall()

                if len(data) == 0:
                    return []
                
                return data

    async def get_active_games(self, user_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM game WHERE bank_id = ? AND banking is TRUE", (user_id))
                data = await cursor.fetchall()

                if len(data) == 0:
                    return []
                
                return data

    async def delete_user_game(self, game_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM game WHERE id = ? AND player_id is NULL", (game_id,))
                data = await cursor.fetchone()

                if data is None:
                    return False, 0
                
                await cursor.execute("DELETE FROM game WHERE id = ?", (game_id,))
                await connection.commit()
                
                return True, data[2]

    async def delete_game(self, game_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM game WHERE id = ?", (game_id,))
                data = await cursor.fetchone()

                if data is None:
                    return False
                
                await cursor.execute("DELETE FROM game WHERE id = ?", (game_id,))
                await connection.commit()
                
                return True

    async def get_free_games(self, user_id, page = 0, type = 1):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM game WHERE player_id is NULL AND bank_id != ? AND game_type = ? LIMIT 5 OFFSET ?", (user_id, type, page*5,))
                data = await cursor.fetchall()
                
                if len(data) == 0:
                    return []
                
                return data

    async def set_banking(self, banking: bool, game_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE game SET banking = ? WHERE id = ?", (banking, game_id))
                await connection.commit()
                return True

    async def add_player(self, game_id, user_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                if await self.check_game(game_id) is False:
                    return False
                    
                await cursor.execute("UPDATE game SET player_id = ? WHERE id = ?", (user_id, game_id))
                await connection.commit()
                return True

    async def add_score(self, game_id, score, user = "bank"):
        """
            user can be bank and player
        """
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"UPDATE game SET {user}_score = {user}_score + ?, {user}_step = {user}_step + 1 WHERE id = ?", (score, game_id))
                await connection.commit()
                return True

    async def get_game_count(self, user_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT COUNT(*) FROM game WHERE player_id = ? OR bank_id = ?", (user_id, user_id,))
                count = await cursor.fetchone()
                
                return count[0]

    async def get_score(self, game_id, user = "bank"):
        """
            User can be bank or player
        """
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT {user}_score FROM game WHERE id = ?", (game_id,))
                data = await cursor.fetchone()

                if data is None:
                    return None

                return data[0]

    async def get_step(self, game_id, user = "bank"):
        """
            User can be bank or player
        """
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT {user}_step FROM game WHERE id = ?", (game_id,))
                data = await cursor.fetchone()

                if data is None:
                    return None

                return data[0]

    async def get_bet(self, game_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT bet FROM game WHERE id = ?", (game_id,))
                data = await cursor.fetchone()

                if data is None:
                    return None

                return data[0]

    async def get_banking(self, game_id):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT banking FROM game WHERE id = ?", (game_id,))
                data = await cursor.fetchone()

                if data is None:
                    return None

                return bool(data[0])

    async def get_last_id(self):
        async with aiosqlite.connect('database/game.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT seq FROM sqlite_sequence WHERE name = 'game'")
                data = await cursor.fetchone()
                if data is None:
                    return None
                return data[0]
