from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from create_bot import _

from database.game_db import Game

from utils.other import get_game_emoji

game_db = Game()

async def get_game_button(user_id, page: int = 0, type = 1) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    
    games = await game_db.get_free_games(user_id, page, type)
    
    emoji = await get_game_emoji(type)
    
    if len(games) == 0:
        markup.row(
            InlineKeyboardButton(
                text=_('😢 Активных игр сейчас нет'),
                callback_data=f'main_start_back_button'),
            width=1)

    for game in games:
        markup.row(
            InlineKeyboardButton(
                text=_('{} #Game_{} | Сумма {} LAVE').format(emoji, game[0], game[2]),
                callback_data=f'{game[0]}_start_game_button'),
            width=1)

    markup.row(
        InlineKeyboardButton(text='<<',callback_data=f'{page}_{type}_game_back_page'),
        InlineKeyboardButton(text='>>',callback_data=f'{page}_{type}_game_next_page'),
        width=2)
    
    markup.row(
        InlineKeyboardButton(text=_('🃏 21 очко'),callback_data='1_game_type_button'),
        InlineKeyboardButton(text=_('🎲 Кости'),callback_data='2_game_type_button'),
        width=2)
    
    markup.row(
        InlineKeyboardButton(text=_('🕹️ Создать'),callback_data='create_game_button'),
        width=1
    )

    markup.row(
        InlineKeyboardButton(text=_('🗂 Мои игры'),callback_data='my_games_button'),
        InlineKeyboardButton(text=_('↪️ Обновить'),callback_data='update_button'),
        width=2
        )

    markup.row(
        InlineKeyboardButton(text=_("назад"), callback_data="main_start_back_button"), 
        width=1
        )

    return markup.as_markup(resize_keyboard=True)

async def get_mygame_button(user_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
        
    games = await game_db.get_user_games(user_id)
    
    if len(games) == 0:
        markup.row(
            InlineKeyboardButton(
                text=_('😢 Вы не создали игры'),
                callback_data=f'update_button'),
            width=1)

    for game in games:
        emoji = await get_game_emoji(game[1])
        markup.row(
            InlineKeyboardButton(
                text=_('❌ | {} #Game_{} | Сумма {} LAVE').format(emoji, game[0], game[2]),
                callback_data=f'{game[0]}_delete_game_button'),
            width=1)

    markup.row(
        InlineKeyboardButton(text=_("назад"), callback_data="update_button"), 
        width=1
        )

    return markup.as_markup(resize_keyboard=True)

async def get_game_type_button() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    markup.row(
        InlineKeyboardButton(text=_('🃏 21 очко'),callback_data=f'1_game_choose_button'),
        InlineKeyboardButton(text=_('🎲 Кости'),callback_data=f'2_game_choose_button'),
        width=2
    )
    
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