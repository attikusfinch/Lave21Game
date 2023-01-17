from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from create_bot import _

from utils.wallet_links import *

async def get_deposit_buttons(user_id):
    markup = InlineKeyboardBuilder()
    
    markup.row(
            InlineKeyboardButton(text=_("TonKeeper"), callback_data="_"), 
            width=1)
    
    markup.row(
            InlineKeyboardButton(text=_("Отправить LAVE"), url=send_tonkeeper_lave(user_id)), 
            InlineKeyboardButton(text=_("Отправить TON"), url=send_tonkeeper_ton(user_id)),
            width=2)
    
    markup.row(
            InlineKeyboardButton(text=_("Другое"), callback_data="_"), 
            width=1)
    
    markup.row(
            InlineKeyboardButton(text=_("Отправить LAVE"), url=send_lave(user_id)), 
            InlineKeyboardButton(text=_("Отправить TON"), url=send_ton(user_id)),
            width=2)
    
    markup.row(
            InlineKeyboardButton(text=_("назад"), callback_data="profile_button"), 
            width=1)
    
    return markup.as_markup(resize_keyboard=True)

async def get_withdraw_buttons(user_id):
    markup = InlineKeyboardBuilder()
    
    markup.row(
            InlineKeyboardButton(text=_("✅ Подтвердить"), callback_data="comfirm_withdraw_button"), 
            width=1)
    
    markup.row(
            InlineKeyboardButton(text=_("❌ Отменить"), callback_data="cancel_withdraw_button"),
            width=1)
    
    return markup.as_markup(resize_keyboard=True)