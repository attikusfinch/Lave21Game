from aiogram import types
from aiogram import Router
from keyboard.main_button import *
from database.wallet_db import Wallet
from database.game_db import Game
from create_bot import _
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from handlers.game.states import GameState

from keyboard.cancel_button import *

from keyboard.game_button import get_game_button

start_game_router = Router()

wallet_db = Wallet()
game_db = Game()

@start_game_router.callback_query(F.data.in_({"play_button", "update_button"}))
async def get_games(ctx: types.CallbackQuery):
    user_id = ctx.from_user.id
    
    try:
        await ctx.message.edit_text(
            _("<b>🎰 Доступные игры</b>"), 
            parse_mode="HTML",
            reply_markup=await get_game_button(user_id)
        )
    except:
        await ctx.answer(_("🥲 Новых игр не найдено"))

@start_game_router.callback_query(F.data == "create_game_button")
async def set_game(ctx: types.CallbackQuery, state: FSMContext):
    user_id = ctx.from_user.id
    
    balance = await wallet_db.get_lave(user_id)

    await ctx.message.edit_text(
        _("<b>💵 Укажите сумму LAVE для создания игры (Минимум 1000)</b>" + "\n" + 
          "--------------------------" + "\n" + 
          "<i>💰 LAVE: {}</i>").format(balance), 
        parse_mode="HTML",
        reply_markup=await get_game_cancel_button()
    )

    await state.set_state(GameState.get_lave_count)

@start_game_router.message(GameState.get_lave_count)
async def start_game(ctx: types.Message, state: FSMContext):
    lave_bet = ctx.text
    
    user_id = ctx.from_user.id
    
    balance = await wallet_db.get_lave(user_id)
    game_count = await game_db.get_game_count(user_id)
    
    if isinstance(ctx, types.CallbackQuery):
        await ctx.message.edit_text(_("❕ Отмена"), reply_markup=await get_game_cancel_button())
        await state.clear()
        return
    
    if lave_bet.isdigit() == False:
        await ctx.reply(_("❕ Ошибка, сумма игры должна быть больше 1000 LAVE"), reply_markup=await get_game_cancel_button())
        await state.clear()
        return
    
    lave_bet = int(lave_bet)

    if game_count >= 5:
        await ctx.reply(_("❕ Ошибка, нельзя создать больше 5 игр"), reply_markup=await get_game_cancel_button())
        await state.clear()
        return
    
    if balance is None:
        await ctx.reply(_("❕ Ошибка, введите /start"), reply_markup=await get_game_cancel_button())
        await state.clear()
        return
    
    if lave_bet < 1000:
        await ctx.reply(_("❕ Ошибка, сумма игры должна быть больше 1000 LAVE"), reply_markup=await get_game_cancel_button())
        await state.clear()
        return

    if lave_bet > balance:
        await ctx.reply(_("❕ Ошибка, на вашем балансе недостаточно LAVE"), reply_markup=await get_game_cancel_button())
        await state.clear()
        return
        
    await wallet_db.set_lave(user_id, lave_bet, False)
    await game_db.add_game(lave_bet, user_id)
    
    message = _("🃏 Игра создана, ожидайте соперника.")
    
    if isinstance(ctx, types.CallbackQuery):
        await ctx.message.reply(
            message,
            reply_markup=await get_game_button(user_id)
        )

        await state.clear()
        return

    await ctx.reply(
        message,
        reply_markup=await get_game_button(user_id)
    )
    
    await state.clear()

@start_game_router.callback_query(F.data.endswith("_game_next_page"))
async def next_page(ctx: types.CallbackQuery):
    page =int(ctx.data.split("_")[0])
    user_id = ctx.from_user.id
        
    data = await get_game_button(user_id, page+1)
    
    if data is not None and len(data.inline_keyboard) > 6:
        await ctx.message.edit_reply_markup(reply_markup=data)
    else:
        await ctx.answer(_("Дальше пусто"))

@start_game_router.callback_query(F.data.endswith("_game_back_page"))
async def prev_page(ctx: types.CallbackQuery):
    page =int(ctx.data.split("_")[0])
    user_id = ctx.from_user.id
    
    if page < 1:
        await ctx.answer(_("Дальше пусто"))
        return
    
    data = await get_game_button(user_id, page-1)
    
    if data is not None and len(data.inline_keyboard) > 6:
        await ctx.message.edit_reply_markup(reply_markup=data)
    else:
        await ctx.answer(_("Дальше пусто"))