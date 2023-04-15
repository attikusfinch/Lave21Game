from aiogram import types
from aiogram import Router
from create_bot import dp, i18n
from keyboard.main_button import *
from database.users_db import Users
from database.wallet_db import Wallet
from database.stats_db import Stats, GlobalStats
from create_bot import _
from aiogram.filters import Command
from handlers.commands.bot_commands import BaseCommands
from aiogram import F, Router

from aiogram.utils.i18n import I18n
from settings import I18N_DOMAIN, LOCALES_DIR

main_router = Router()

user_db = Users()
stat_db = Stats()
global_stat_db = GlobalStats()
wallet_db = Wallet()

@main_router.message(Command(BaseCommands.SETTINGS))
@main_router.callback_query(F.data == "settings_button")
async def settings(ctx):
    user_id = ctx.from_user.id
    
    if isinstance(ctx, types.CallbackQuery):
        await ctx.message.edit_text(
            _("<i>🌍 Выберите язык</i>"), 
            parse_mode="HTML", 
            reply_markup=await get_language_buttons(user_id)
        )
        return

    await dp.send_message(ctx.from_user.id, 
        _("<i>🌍 Выберите язык</i>"), 
        parse_mode="HTML", 
        reply_markup=await get_language_buttons(user_id)
    )

@main_router.message(Command(BaseCommands.START))
@main_router.callback_query(F.data == "main_start_back_button")
@main_router.callback_query(F.data.endswith("_lang_button"))
async def start(ctx: types.CallbackQuery):
    user_id = ctx.from_user.id
    
    language = None
    
    if isinstance(ctx, types.CallbackQuery):
        if ctx.data.endswith("_lang_button"):
            language = ctx.data.split("_")[0]
            
            await user_db.add_user(user_id, language)
            await stat_db.add_stats(user_id)
            await wallet_db.add_wallet(user_id, 0, 0)

    if await user_db.get_language(user_id) is None:
        await settings(ctx)
        return
    
    if language is not None:
        # костыль, надо подпарвить как-то
        i18n_new = I18n(path=LOCALES_DIR, default_locale=language, domain=I18N_DOMAIN)
        i18n.i18n.set_current(i18n_new)
        
    if isinstance(ctx, types.CallbackQuery):
        await ctx.message.edit_text(
            _("👑 Добро пожаловать, <b>{}</b>").format(ctx.from_user.username), 
            parse_mode="HTML", 
            reply_markup=await get_start_buttons(user_id)
        )
        return

    await dp.send_message(ctx.from_user.id, 
            _("👑 Добро пожаловать, <b>{}</b>").format(ctx.from_user.username), 
            parse_mode="HTML", 
            reply_markup=await get_start_buttons(user_id)
        )

@main_router.callback_query(F.data == "info_button")
async def info(ctx: types.CallbackQuery):
    user_id = ctx.from_user.id
    
    game_count = await global_stat_db.get_game_count()
    lave_count = await global_stat_db.get_lave_count()

    await ctx.message.edit_text(
            _("На данный момент пользователи сыграли {} игр на сумму {} LAVE.").format(game_count, lave_count), 
            parse_mode="HTML", 
            reply_markup=await get_info_buttons(user_id)
        )

@main_router.callback_query(F.data == "profile_button")
async def profile(ctx: types.CallbackQuery):
    user_id = ctx.from_user.id
    
    lave_balance = await wallet_db.get_lave(user_id)
    ton_balance = await wallet_db.get_ton(user_id)
    withdraw_wallet = await wallet_db.get_wallet(user_id)
    
    if withdraw_wallet is None:
        withdraw_wallet = "Нету"
    
    stat_game, stat_win, stat_lose = await stat_db.get_stats(user_id)
    
    await ctx.message.edit_text(
        _("🔐 id: <code>{}</code>" + "\n\n" +
        "<b>💰 Баланс:</b>" + "\n" +
        "╠ <code>{}</code> <a href='https://t.me/lavetoken'>Lavandos, (LAVE)</a>" + "\n" +
        "╚ <code>{}</code> <a href='https://ton.org'>The Open Network, (TON)</a>" + "\n\n" +
        "<b>👛 Привязанный кошелек:</b>" + "\n" +
        "<code>{}</code>" + "\n\n" +
        "<b>📊 Статистика:</b>" + "\n" +
        "╠ Игры: <code>{}</code>" + "\n" +
        "╠ Победы: <code>{}</code>" + "\n" +
        "╚ Прогрыши: <code>{}</code>").format(
            ctx.from_user.id,
            lave_balance,
            ton_balance,
            withdraw_wallet,
            stat_game,
            stat_win,
            stat_lose),
        parse_mode="HTML",
        reply_markup=await get_profile_buttons(user_id),
        disable_web_page_preview=True
    )