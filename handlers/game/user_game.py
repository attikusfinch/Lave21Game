from aiogram import types
from aiogram import Router
from keyboard.main_button import *
from create_bot import _
from aiogram import F, Router
from database.game_db import Game, Poker, Dice
from database.wallet_db import Wallet

from keyboard.cancel_button import *

from keyboard.game_button import get_mygame_button

mygame_router = Router()

game_db = Game()
dice_db = Dice()
poker_db = Poker()

wallet_db = Wallet()

@mygame_router.callback_query(F.data.in_({"my_games_button"}) | F.data.endswith("_my_games_button"))
async def get_my_games(ctx: types.CallbackQuery):
    user_id = ctx.from_user.id
    
    game_type = False
    
    msg = (_("<b>🎰 Ваши игры</b>" + "\n" + 
            "--------------------------" + "\n"))
    
    if ctx.data.split("_")[0].isdigit():
        game_type = bool(int(ctx.data.split("_")[0]))
        msg += _("<i>Выберите игру, которую вы хотите продолжить. Помните! Что при продолжении, вы автоматически возьмете 1 карту.</i>")
    else:
        msg += _("<i>Выберите игру, которую вы хотите удалить</i>")
    
    try:
        await ctx.message.edit_text(
            msg, 
            parse_mode="HTML",
            reply_markup=await get_mygame_button(user_id, game_type)
        )
    except:
        await ctx.answer(_("🥲 Новых игр не найдено"))

@mygame_router.callback_query(F.data.endswith("_delete_game_button"))
async def delete_my_game(ctx: types.CallbackQuery):
    user_id = ctx.from_user.id
    game_id = ctx.data.split("_")[0]
    
    data, amount = await game_db.delete_user_game(game_id)
    
    game_type = await game_db.get_game_type(game_id)

    if game_type == 1:
        await poker_db.delete_game(game_id)
    elif game_type == 2:
        await dice_db.delete_game(game_id)
    
    if data is False:
        await ctx.message.edit_text(
            _("❌ Активную игру отменить нельзя"),
            reply_markup=await get_mygame_button(user_id))
        return
    
    await wallet_db.set_lave(user_id, amount, True)
    
    await ctx.message.edit_text(
        _("❌ Игра отменена"),
        reply_markup=await get_mygame_button(user_id))