import aiosqlite

async def create_user_table():
    print("-User db init")
    async with aiosqlite.connect('database/users.db') as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    lang STRING NOT NULL
                );
            """)
            await connection.commit()

async def create_wallet_table():
    print("-Wallet db init")
    async with aiosqlite.connect('database/wallet.db') as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS wallet (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    lave_count FLOAT NOT NULL,
                    ton_count FLOAT NOT NULL,
                    withdraw_address STRING
                );
            """)
            await connection.commit()

async def create_statistic_table():
    print("-Statistic db init")
    async with aiosqlite.connect('database/stats.db') as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    game_count INTEGER NOT NULL,
                    win_count INTEGER NOT NULL,
                    lose_count INTEGER NOT NULL
                );
            """)
            
            await connection.commit()
            
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS global_stats (
                    game_count INTEGER NOT NULL,
                    lave_count INTEGER NOT NULL
                );
            """)

            await cursor.execute("SELECT game_count FROM global_stats")
            data = await cursor.fetchone()
            
            if data is None:
                await cursor.execute("INSERT INTO global_stats (game_count, lave_count) VALUES (0, 0);")

            await connection.commit()

async def create_game_table():
    print("-Game db init")
    async with aiosqlite.connect('database/game.db') as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS game (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_type INTEGER NOT NULL,
                    bet INTEGER NOT NULL,
                    creator_id INTEGER NOT NULL,
                    player_id INTEGER
                );
            """)

            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS poker(
                    id INTEGER NOT NULL,
                    banking BOOL,
                    bank_step INTEGER NOT NULL,
                    player_step INTEGER NOT NULL,
                    bank_score INTEGER NOT NULL,
                    player_score INTEGER NOT NULL
                );
            """)
            
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS dice(
                    id INTEGER NOT NULL,
                    bank_score INTEGER NOT NULL,
                    player_score INTEGER NOT NULL
                );
            """)
            
            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS rps(
                    id INTEGER NOT NULL,
                    bank_score INTEGER,
                    player_score INTEGER,
                    bank_choose INTEGER,
                    player_choose INTEGER
                );
                """
            )

            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS treasure(
                    id INTEGER NOT NULL,
                    treasure_field STRING NOT NULL,
                    bank_score INTEGER,
                    player_score INTEGER
                );
                """
            )

            await connection.commit()

async def create_transaction_table():
    print("-transaction db init")
    async with aiosqlite.connect('database/transactions.db') as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS transaction_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jetton_date TEXT NOT NULL,
                    jetton_comment TEXT NOT NULL
                );
            """)
            await connection.commit()

async def create_withdraw_table():
    print("-withdraw db init")
    async with aiosqlite.connect('database/withdraw.db') as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS withdraw_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    withdraw_address TEXT NOT NULL,
                    amount INTEGER NOT NULL
                );
            """)
            await connection.commit()

# Товарищи. Я пока оставлю так, но это можно засунуть в каждую orm в __init__ функцию.

async def init():
    await create_user_table()
    await create_statistic_table()
    await create_wallet_table()
    await create_game_table()
    await create_transaction_table()
    await create_withdraw_table()

async def create_db():
    await init()