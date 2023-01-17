from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from create_bot import _

async def get_main_button() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    
    markup.row(InlineKeyboardButton(text=_("назад"), callback_data="main_start_back_button"), width=1)

    return markup.as_markup(resize_keyboard=True)

async def get_info_button() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    
    markup.row(InlineKeyboardButton(text=_("назад"), callback_data="info_button"), width=1)

    return markup.as_markup(resize_keyboard=True)

async def get_game_cancel_button() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    markup.row(InlineKeyboardButton(text=_("назад"), callback_data="play_button"), width=1)

    return markup.as_markup(resize_keyboard=True)

async def get_cancel_button() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    
    markup.row(InlineKeyboardButton(text=_("назад"), callback_data="cancel_button"), width=1)

    return markup.as_markup(resize_keyboard=True)

async def get_profile_button() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    
    markup.row(InlineKeyboardButton(text=_("назад"), callback_data="profile_button"), width=1)
    
    return markup.as_markup(resize_keyboard=True)