from aiogram import types
from aiogram import Router
from keyboard.main_button import *
from database.stats_db import Stats
from create_bot import _
from aiogram import F, Router

from keyboard.cancel_button import *

from create_bot import dp

start_rating_router = Router()

stats_db = Stats()

@start_rating_router.callback_query(F.data == "rating_button")
async def rating(ctx: types.CallbackQuery):
    user_id = ctx.from_user.id

    users = await stats_db.get_top_players(10)
    rank = await stats_db.get_player_rating(user_id)

    top = ""

    for user in users:
        try:
            name = (await dp.get_chat(user[1])).username
        except:
            name = user[1]

        top += f"ℹ️ {name} | 🕹 {user[2]} | 🏆 {user[3]} | ☹️ {user[4]}\n"
    
    await ctx.message.edit_text(
        f"<b>🏆 Топ-10 игроков</b> \n\n" +
        f"{top}" + 
        "--------------------------" + "\n" +
        f"🏅 Ты на <b>{rank}</b> месте", parse_mode="HTML",reply_markup=await get_info_button()
    )