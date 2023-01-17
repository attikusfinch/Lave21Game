from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from create_bot import _

from utils.wallet_links import send_lave, send_ton

async def get_deposit_buttons(user_id):
    markup = InlineKeyboardBuilder()
    
    markup.row(
            InlineKeyboardButton(text=_("Отправить LAVE"), url=send_lave(user_id)), 
            width=1)
    
    markup.row(
            InlineKeyboardButton(text=_("Отправить TON"), url=send_ton(user_id)),
            width=1)
    
    markup.row(
            InlineKeyboardButton(text="назад", callback_data="profile_button"), 
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