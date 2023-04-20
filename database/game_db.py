import aiosqlite
import asyncio

class Game(object):
    def __init__(self):
        self.connection : aiosqlite.Connection = None
        self.cursor : aiosqlite.Cursor = None
        self.name = "game"
        asyncio.run(self.connect())

    async def connect(self):
        self.connection = await aiosqlite.connect(f'database/game.db')
        self.cursor = await self.connection.cursor()

    async def add_game(self, creator_id, bet, game_type) -> int:
        """Create game into the main db

        Args:
            creator_id (int): user who create game
            bet (int): bet for a game
            game_type (int): 1 - poker, 2 - dice, ...

        Returns:
            int: id of created game for connect with others db's
        """
        await self.cursor.execute(f"INSERT INTO {self.name} (bet, creator_id, player_id, game_type) VALUES (?, ?, ?, ?)", (bet, creator_id, None, game_type,))
        await self.connection.commit()
        
        game_id = await self.cursor.execute("SELECT seq FROM sqlite_sequence")
        game_id = await game_id.fetchone()
        
        return game_id[0]
    
    async def get_active_games(self, user_id):
        await self.cursor.execute(f"SELECT * FROM game g JOIN poker p ON g.id = p.id WHERE g.creator_id = ? AND p.banking = 1", (user_id,))
        data = await self.cursor.fetchall()

        if len(data) == 0:
            return []
        
        return data

    async def get_game(self, game_id):
        await self.cursor.execute(f"SELECT * FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return data

    async def get_game_type(self, game_id):
        await self.cursor.execute("SELECT game_type FROM game WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return data[0]

    async def get_creator_id(self, game_id):
        await self.cursor.execute(f"SELECT creator_id FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return data[0]

    async def get_player_id(self, game_id):
        await self.cursor.execute(f"SELECT player_id FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return data[0]

    async def check_game(self, game_id):
        await self.cursor.execute(f"SELECT * FROM {self.name} WHERE id = ? AND player_id is NULL", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return False

        return True

    async def get_user_games(self, user_id):
        await self.cursor.execute(f"SELECT * FROM {self.name} WHERE creator_id = ? AND player_id is NULL", (user_id,))
        data = await self.cursor.fetchall()

        if len(data) == 0:
            return []
        
        return data

    async def delete_user_game(self, game_id):
        await self.cursor.execute(f"SELECT * FROM {self.name} WHERE id = ? AND player_id is NULL", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return False, 0
        
        await self.cursor.execute(f"DELETE FROM {self.name} WHERE id = ?", (game_id,))
        await self.connection.commit()
        
        return True, data[2]

    async def delete_game(self, game_id):
        await self.cursor.execute(f"SELECT * FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return False
        
        await self.cursor.execute(f"DELETE FROM {self.name} WHERE id = ?", (game_id,))
        await self.connection.commit()
        
        return True

    async def get_free_games(self, user_id, page = 0, type = 1):
        await self.cursor.execute(f"SELECT * FROM {self.name} WHERE player_id is NULL AND creator_id != ? AND game_type = ? LIMIT 5 OFFSET ?", (user_id, type, page*5,))
        data = await self.cursor.fetchall()
        
        if len(data) == 0:
            return []
        
        return data

    async def add_player(self, game_id, user_id):
        if await self.check_game(game_id) is False:
            return False

        await self.cursor.execute(f"UPDATE {self.name} SET player_id = ? WHERE id = ?", (user_id, game_id))
        await self.connection.commit()
        return True

    async def get_game_count(self, user_id):
        await self.cursor.execute(f"SELECT COUNT(*) FROM {self.name} WHERE player_id = ? OR creator_id = ?", (user_id, user_id,))
        count = await self.cursor.fetchone()
        
        return count[0]

    async def get_bet(self, game_id):
        await self.cursor.execute(f"SELECT bet FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return data[0]


class Poker(Game):
    def __init__(self):
        self.connection : aiosqlite.Connection = None
        self.cursor : aiosqlite.Cursor = None
        self.name = "poker"
        asyncio.run(self.connect())

    async def add_game(self, id):
        await self.cursor.execute(f"INSERT INTO {self.name} (id, banking, bank_step, player_step, bank_score, player_score) VALUES (?, ?, ?, ?, ?, ?)", (id, False, 0, 0, 0, 0))
        await self.connection.commit()
        return True

    async def get_banking(self, game_id):
        await self.cursor.execute(f"SELECT banking FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return bool(data[0])
    
    async def get_score(self, game_id, user = "bank"):
        """
            User can be bank or player
        """
        await self.cursor.execute(f"SELECT {user}_score FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return data[0]

    async def get_step(self, game_id, user = "bank"):
        """
            User can be bank or player
        """
        await self.cursor.execute(f"SELECT {user}_step FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return data[0]

    async def add_score(self, game_id, score, user = "bank"):
        """
            user can be bank and player
        """
        await self.cursor.execute(f"UPDATE {self.name} SET {user}_score = {user}_score + ?, {user}_step = {user}_step + 1 WHERE id = ?", (score, game_id))
        await self.connection.commit()
        return True

    async def set_banking(self, banking: bool, game_id):
        await self.cursor.execute(f"UPDATE {self.name} SET banking = ? WHERE id = ?", (banking, game_id))
        await self.connection.commit()
        return True

class Dice(Game):
    def __init__(self):
        self.connection : aiosqlite.Connection = None
        self.cursor : aiosqlite.Cursor = None
        self.name = "dice"
        asyncio.run(self.connect())
        
    async def add_game(self, game_id):
        await self.cursor.execute(f"INSERT INTO {self.name} (id, bank_score, player_score) VALUES (?, ?, ?)", (game_id, 0, 0,))
        await self.connection.commit()
        return True

    async def add_score(self, game_id, score, user = "bank"):
        """
            user can be bank and player
        """
        await self.cursor.execute(f"UPDATE {self.name} SET {user}_score = {user}_score + ? WHERE id = ?", (score, game_id))
        await self.connection.commit()
        return True

    async def get_score(self, game_id, user = "bank"):
        """
            User can be bank or player
        """
        await self.cursor.execute(f"SELECT {user}_score FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return data[0]
    
class Treasure(Game):
    def __init__(self):
        self.connection : aiosqlite.Connection = None
        self.cursor : aiosqlite.Cursor = None
        self.name = "treasure"
        asyncio.run(self.connect())
        
    async def add_game(self, game_id, field):
        await self.cursor.execute(f"INSERT INTO {self.name} (id, bank_score, player_score, treasure_field) VALUES (?, ?, ?, ?)", (game_id, 0, 0, field,))
        await self.connection.commit()
        return True

    async def add_score(self, game_id, score, user = "bank"):
        """
            user can be bank and player
        """
        await self.cursor.execute(f"UPDATE {self.name} SET {user}_score = {user}_score + ? WHERE id = ?", (score, game_id))
        await self.connection.commit()
        return True
    
    async def add_field(self, game_id, field):
        """
            user can be bank and player
        """
        await self.cursor.execute(f"UPDATE {self.name} SET treasure_field = ? WHERE id = ?", (field, game_id))
        await self.connection.commit()
        return True

    async def get_score(self, game_id, user = "bank"):
        """
            User can be bank or player
        """
        await self.cursor.execute(f"SELECT {user}_score FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return data[0]

    async def get_field(self, game_id):
        """
            User can be bank or player
        """
        await self.cursor.execute(f"SELECT treasure_field FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return data[0]
    

class Rps(Game):
    def __init__(self):
        self.connection : aiosqlite.Connection = None
        self.cursor : aiosqlite.Cursor = None
        self.name = "rps"
        asyncio.run(self.connect())
        
    async def add_game(self, game_id):
        await self.cursor.execute(f"INSERT INTO {self.name} (id, bank_score, player_score, bank_choose, player_choose) VALUES (?, ?, ?, ?, ?)", (game_id, 0, 0, 0, 0,))
        await self.connection.commit()
        return True

    async def add_score(self, game_id, score, user = "bank"):
        """
            user can be bank and player
        """
        await self.cursor.execute(f"UPDATE {self.name} SET {user}_score = {user}_score + ? WHERE id = ?", (score, game_id))
        await self.connection.commit()
        return True
    
    async def add_choose(self, game_id, choose, user = "bank"):
        """
            user can be bank and player
            
            1 - rock
            2 - paper
            3 - scissors
        """
        await self.cursor.execute(f"UPDATE {self.name} SET {user}_choose = ? WHERE id = ?", (choose, game_id))
        await self.connection.commit()
        return True

    async def get_score(self, game_id, user = "bank"):
        """
            User can be bank or player
        """
        await self.cursor.execute(f"SELECT {user}_score FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return data[0]
    
    async def get_choose(self, game_id, user = "bank"):
        """
            User can be bank or player
        """
        await self.cursor.execute(f"SELECT {user}_choose FROM {self.name} WHERE id = ?", (game_id,))
        data = await self.cursor.fetchone()

        if data is None:
            return None

        return data[0]