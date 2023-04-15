from aiogram import types
from aiogram import Router
from keyboard.main_button import *
from database.wallet_db import Wallet
from database.withdraw_db import WithdrawHistory
from create_bot import _
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from keyboard.cancel_button import *

from keyboard.withdraw_button import get_withdraw_buttons
from handlers.profile.states import WithdrawState

from keyboard.cancel_button import *


withdraw_router = Router()

wallet_db = Wallet()
withdraw_db = WithdrawHistory()

@withdraw_router.callback_query(F.data == "withdraw_button")
async def withdraw(ctx: types.CallbackQuery, state: FSMContext):
    user_id = ctx.from_user.id

    wallet = await wallet_db.get_wallet(user_id)
    if wallet is None:
        await ctx.message.edit_text(_("👛 Привяжите кошелек"), reply_markup=await get_profile_button())
        await state.clear()
        return
    
    withdraw = await withdraw_db.get_withdraw_address(user_id)
    if withdraw is not None:
        await ctx.message.edit_text(_("👛 Вы уже создали запрос на вывод"), reply_markup=await get_profile_button())
        await state.clear()
        return

    await ctx.message.edit_text(
        _("📤 Введите сумму LAVE для вывода"),
        parse_mode="HTML",
        reply_markup=await get_cancel_button()
        )
    
    await state.set_state(WithdrawState.get_amount)

@withdraw_router.message(WithdrawState.get_amount)
async def get_amount(ctx: types.Message, state: FSMContext):
    user_id = ctx.from_user.id

    if isinstance(ctx, types.CallbackQuery):
        await ctx.message.edit_text(_("❌ Отмена"), reply_markup=await get_profile_button())
        await state.clear()
        return

    amount = ctx.text
    
    if amount.isdigit() is False:
        await ctx.reply(_("❌ Количество должно быть числом"), reply_markup=await get_profile_button())
        await state.clear()
        return
    
    amount = int(amount)
    
    await state.update_data(amount=amount)
    
    if amount < 100:
        await ctx.reply(_("❌ Сумма должна быть больше 100 LAVE"), reply_markup=await get_profile_button())
        await state.clear()
        return
    
    ton = await wallet_db.get_ton(user_id)
    if ton < 0.05:
        await ctx.reply(_("❌ Недостаточно TON для вывода"), reply_markup=await get_profile_button())
        await state.clear()
        return
    
    lave = await wallet_db.get_lave(user_id)
    if lave < amount:
        await ctx.reply(_("❌ Недостаточно LAVE для вывода"), reply_markup=await get_profile_button())
        await state.clear()
        return
    
    wallet = await wallet_db.get_wallet(user_id)

    await ctx.reply(
        _("<b>📤 Подтверждение вывода</b>" + "\n" + "\n" +

        "Сумма: <code>{}</code> LAVE" + "\n" + 
        "Комиссия: <code>0.05</code> TON" + "\n" +
        "Адрес: <code>{}</code>").format(amount, wallet),
        parse_mode="HTML",
        reply_markup=await get_withdraw_buttons(user_id)
        )
    
    await state.set_state(WithdrawState.get_approve)

@withdraw_router.callback_query(WithdrawState.get_approve, F.data == "comfirm_withdraw_button")
async def accept_approve(ctx: types.CallbackQuery, state: FSMContext):
    user_id = ctx.from_user.id
    
    data = await state.get_data()
    
    amount = data["amount"]
    
    wallet = await wallet_db.get_wallet(user_id)
    
    await wallet_db.set_lave(user_id, amount, False)
    await wallet_db.set_ton(user_id, 0.05, False)
    
    await withdraw_db.set_withdraw(user_id, wallet, amount)
    
    await ctx.message.edit_text(_("{} LAVE скоро будут переведены на ваш кошелек 👛").format(amount), parse_mode="HTML")
    await state.clear()

@withdraw_router.callback_query(WithdrawState.get_approve, F.data == "cancel_withdraw_button")
async def cancel_approve(ctx: types.CallbackQuery, state: FSMContext):
    user_id = ctx.from_user.id
    
    await ctx.message.edit_text(_("❌ Отмена"), parse_mode="HTML", reply_markup=await get_profile_button())
    await state.clear()