from create_bot import bot, dp
from data import create_db
from aiogram import types

from handlers.start.main import main_router
from handlers.profile.wallet import wallet_router
from handlers.profile.deposit import deposit_router
from handlers.game.create_game import game_router
from handlers.game.user_game import mygame_router
from handlers.other.rating import rating_router
from handlers.game.play_game import main_game_menu_router
from handlers.profile.withdraw import withdraw_router
from handlers.game.minigames.poker import poker_router
from handlers.game.minigames.dice import dice_router

import asyncio

async def set_up_commands(dp):
    await dp.set_my_commands([
        types.BotCommand("start", "Start bot")
    ])

async def register():
    await create_db()

    bot.include_router(main_router)
    bot.include_router(wallet_router)
    bot.include_router(game_router)
    bot.include_router(poker_router)
    bot.include_router(dice_router)
    bot.include_router(rating_router)
    bot.include_router(mygame_router)
    bot.include_router(main_game_menu_router)
    bot.include_router(deposit_router)
    bot.include_router(withdraw_router)

    try:
        await bot.start_polling(dp)
    except Exception as e:
        await dp.session.close()
        await bot.storage.close()
        raise e

if __name__ == "__main__":
    asyncio.run(register())