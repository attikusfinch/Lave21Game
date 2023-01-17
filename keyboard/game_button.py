from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from create_bot import _

from database.game_db import Game

async def get_game_button(user_id, page: int = 0) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    
    game_db = Game()
    
    games = await game_db.get_free_games(user_id, page)
    
    if len(games) == 0:
        markup.row(
            InlineKeyboardButton(
                text=_('😢 Активных игр сейчас нет'),
                callback_data=f'main_start_back_button'),
            width=1)

    for game in games:
        markup.row(
            InlineKeyboardButton(
                text=_('🎲 #Game_{} | Сумма {} LAVE').format(game[0], game[1]),
                callback_data=f'{game[0]}_start_game_button'),
            width=1)

    markup.row(
        InlineKeyboardButton(text='<<',callback_data=f'{page}_game_back_page'),
        InlineKeyboardButton(text='>>',callback_data=f'{page}_game_next_page'),
        width=2)

    markup.row(
        InlineKeyboardButton(text=_('🃏 Мои игры'),callback_data='my_games_button'),
        InlineKeyboardButton(text=_('↪️ Обновить'),callback_data='update_button'),
        width=2)

    markup.row(
        InlineKeyboardButton(text=_('🕹️ Создать игру'),callback_data='create_game_button'),
        width=1
        )

    markup.row(
        InlineKeyboardButton(text=_("назад"), callback_data="main_start_back_button"), 
        width=1
        )

    return markup.as_markup(resize_keyboard=True)

async def get_mygame_button(user_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    
    game_db = Game()
    
    games = await game_db.get_user_games(user_id)
    
    if len(games) == 0:
        markup.row(
            InlineKeyboardButton(
                text=_('😢 Вы не создали игры'),
                callback_data=f'update_button'),
            width=1)

    for game in games:
        markup.row(
            InlineKeyboardButton(
                text=_('❌ | 🎲 #Game_{} | Сумма {} LAVE').format(game[0], game[1]),
                callback_data=f'{game[0]}_delete_game_button'),
            width=1)

    markup.row(
        InlineKeyboardButton(text=_("назад"), callback_data="update_button"), 
        width=1
        )

    return markup.as_markup(resize_keyboard=True)

async def get_gaming_button(game_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    
    markup.row(
        InlineKeyboardButton(text=_('➕ Взять еще карту'),callback_data=f'{game_id}_add_card_button'),
        width=1
    )
    
    markup.row(
        InlineKeyboardButton(text=_('✔️ Хватит, пусть играет'),callback_data=f'{game_id}_pass_button'),
        width=1
    )
    
    return markup.as_markup(resize_keyboard=True)

async def get_banking_button(game_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    
    markup.row(
        InlineKeyboardButton(text=_('➕ Взять еще карту'),callback_data=f'{game_id}_add_card_button'),
        width=1
    )
    
    markup.row(
        InlineKeyboardButton(text=_('✔️ Хватит, вскрываемся'),callback_data=f'{game_id}_end_game_button'),
        width=1
    )
    
    return markup.as_markup(resize_keyboard=True)