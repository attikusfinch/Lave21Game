from create_bot import bot, dp
from data import create_db
from aiogram import types

from handlers.start.main import start_main_router
from handlers.profile.wallet import start_wallet_router
from handlers.profile.deposit import start_deposit_router
from handlers.game.create import start_game_router
from handlers.game.mygames import start_mygame_router
from handlers.other.rating import start_rating_router
from handlers.game.play import start_play_game_router
from handlers.profile.withdraw import start_withdraw_router

import asyncio

async def set_up_commands(dp):
    await dp.set_my_commands([
        types.BotCommand("start", "Start bot")
    ])

async def register():
    await create_db()

    bot.include_router(start_main_router)
    bot.include_router(start_wallet_router)
    bot.include_router(start_game_router)
    bot.include_router(start_rating_router)
    bot.include_router(start_mygame_router)
    bot.include_router(start_play_game_router)
    bot.include_router(start_deposit_router)
    bot.include_router(start_withdraw_router)

    try:
        await bot.start_polling(dp)
    except Exception as e:
        await dp.session.close()
        await bot.storage.close()
        raise e

if __name__ == "__main__":
    asyncio.run(register())