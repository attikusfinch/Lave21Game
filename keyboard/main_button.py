from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from create_bot import _

async def get_language_buttons(user_id : int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    
    markup.row(InlineKeyboardButton(text=f"🇷🇺 русский", callback_data="ru_lang_button"), width=1)
    markup.row(InlineKeyboardButton(text=f"🇬🇧 english", callback_data="en_lang_button"), width=1)

    return markup.as_markup(resize_keyboard=True)

async def get_start_buttons(user_id : int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    
    markup.row(
        InlineKeyboardButton(text=_("🃏 Играть"), callback_data="play_button"),
        InlineKeyboardButton(text=_("🖥 Профиль"), callback_data="profile_button"), 
        width=2)
    
    markup.row(
        InlineKeyboardButton(text=_("📜 Информация"), callback_data="info_button"),
        InlineKeyboardButton(text=_("⚙️ Настройки"), callback_data="settings_button"), 
        width=2)
    
    return markup.as_markup(resize_keyboard=True)

async def get_info_buttons(user_id : int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    
    markup.row(
            InlineKeyboardButton(text=_("🏆 Топ 10 игроков"), callback_data="rating_button"), 
            width=1)
    
    markup.row(
        InlineKeyboardButton(text=_("💬 Чат LAVE"), url="https://t.me/lavetoken"),
        InlineKeyboardButton(text=_("📕 Правила игры"), url="https://telegra.ph/Dvadcat-odno-21Ochko--Pravila-01-08"), 
        width=2)
    
    markup.row(
        InlineKeyboardButton(text=_("⚜️ Купить / продать LAVE"), url="https://telegra.ph/Lave-01-09"),
        width=2
    )
    
    markup.row(
        InlineKeyboardButton(text=_("назад"), callback_data="main_start_back_button"),
        width=1
    )
    
    return markup.as_markup(resize_keyboard=True)

async def get_profile_buttons(user_id: int, wallet=None):
    markup = InlineKeyboardBuilder()

    deposit_button = InlineKeyboardButton(text=_("📥 Пополнить"), callback_data="deposit_button")
    withdraw_button = InlineKeyboardButton(text=_("📥 Вывести"), callback_data="withdraw_button")
    change_wallet_button = InlineKeyboardButton(text=_("👛 Сменить кошелек"), callback_data = f"connect_wallet_button")
    #ref_button = InlineKeyboardButton(text=_("👥 Партнерская программа"), callback_data="referals_button")
    
    back_button = InlineKeyboardButton(text=_("назад"), callback_data="main_start_back_button")

    if wallet is None:
        change_wallet_button = InlineKeyboardButton(text = _('👛 Привязать кошелек'), callback_data = f"connect_wallet_button")

    markup.row(
            deposit_button, 
            withdraw_button,
            width=2)
    
    markup.row(
        change_wallet_button,
        width=1)
    
    markup.row(
        back_button,
        width=1
    )
    
    return markup.as_markup(resize_keyboard=True)