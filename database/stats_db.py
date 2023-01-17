import aiosqlite

class Stats:
    async def add_stats(self, user_id, game_count=0, win_count=0, lose_count=0):
        async with aiosqlite.connect('database/stats.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM stats WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()

                if data is None:
                    await cursor.execute("INSERT INTO stats (user_id, game_count, win_count, lose_count) VALUES (?, ?, ?, ?)", (user_id, game_count, win_count, lose_count))
                    await connection.commit()
                    return True

                return False

    async def get_stats(self, user_id):
        """_summary_

        Args:
            user_id (_type_): _id which uses for get stat_

        Returns:
            _game-count_: _count of played games_
            _win-count_: _count of won games_
            _lose-count_: _count of lost games_
        """
        async with aiosqlite.connect('database/stats.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM stats WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()
                
                if data is None:
                    return None, None, None
                
                return data[2], data[3], data[4]

    async def update_stats(self, user_id: int, win: bool):
        async with aiosqlite.connect('database/stats.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM stats WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()

                if data is None:
                    return None

                if win:
                    await cursor.execute("UPDATE stats SET game_count = game_count + 1, win_count = win_count + 1 WHERE user_id = ?", (user_id,))
                else:
                    await cursor.execute("UPDATE stats SET game_count = game_count + 1, lose_count = lose_count + 1 WHERE user_id = ?", (user_id,))
                await connection.commit()

                return True

    async def get_top_players(self, limit):
        async with aiosqlite.connect('database/stats.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT * FROM stats ORDER BY win_count DESC LIMIT {limit}")
                data = await cursor.fetchall()
                
                if len(data) == 0:
                    return []
                
                return data

    async def get_player_rating(self, user_id):
        # Пожалуйста кто-нибудь сделайте это лучше
        async with aiosqlite.connect('database/stats.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("""
                            SELECT id,
                                (SELECT COUNT(*) FROM stats AS p WHERE p.win_count >= t.win_count) AS position
                            FROM stats AS t WHERE user_id=?;
                    """, (user_id,))
                data = await cursor.fetchone()
                
                if data is None:
                    return None
                
                return data[1]

class GlobalStats:
    async def get_game_count(self):
        async with aiosqlite.connect('database/stats.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT game_count FROM global_stats")
                data = await cursor.fetchone()
                if data is None:
                    return None
                return data[0]

    async def set_game_count(self):
        async with aiosqlite.connect('database/stats.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE global_stats SET game_count = game_count + 1")
                await connection.commit()
                return True

    async def get_lave_count(self):
        async with aiosqlite.connect('database/stats.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT lave_count FROM global_stats")
                data = await cursor.fetchone()
                if data is None:
                    return None
                return data[0]

    async def set_lave_count(self, count):
        async with aiosqlite.connect('database/stats.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE global_stats SET lave_count = lave_count + ?", (count,))
                await connection.commit()
                return True
