from aiogram import types
from aiogram import Router
from keyboard.main_button import *
from create_bot import _
from aiogram import F, Router
from database.game_db import Game
from database.wallet_db import Wallet
from aiogram.fsm.context import FSMContext

from keyboard.cancel_button import *

from keyboard.game_button import get_mygame_button

start_mygame_router = Router()

game_db = Game()
wallet_db = Wallet()

@start_mygame_router.callback_query(F.data.in_({"my_games_button"}))
async def get_my_games(ctx: types.CallbackQuery):
    user_id = ctx.from_user.id
    
    await ctx.message.edit_text(
        _("<b>🎰 Ваши игры</b>" + "\n" + 
          "--------------------------" + "\n" + 
          "<i>Выберите игру, которую вы хотите удалить</i>"), 
        parse_mode="HTML",
        reply_markup=await get_mygame_button(user_id)
    )

@start_mygame_router.callback_query(F.data.endswith("_delete_game_button"))
async def delete_my_game(ctx: types.CallbackQuery):
    user_id = ctx.from_user.id
    game_id = ctx.data.split("_")[0]
    
    data, amount = await game_db.delete_user_game(game_id)
    
    if data is False:
        await ctx.message.edit_text(
            "❌ Активную игру отменить нельзя",
            reply_markup=await get_mygame_button(user_id))
        return
    
    await wallet_db.set_lave(user_id, amount, True)
    
    await ctx.message.edit_text(
        "❌ Игра отменена",
        reply_markup=await get_mygame_button(user_id))