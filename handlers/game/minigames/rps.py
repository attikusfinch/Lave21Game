from keyboard.main_button import *
from database.game_db import Game, Rps
from create_bot import _
from aiogram import Router, F, types

from database.wallet_db import Wallet
from database.stats_db import Stats, GlobalStats
from keyboard.game_button import get_rps_button

from keyboard.cancel_button import *

from create_bot import dp

import asyncio
from handlers.game import play_game

rps_router = Router()

game_db = Game()
rps_db = Rps()

wallet_db = Wallet()
stats_db = Stats()
global_stats_db = GlobalStats()

async def rps_game(ctx, game_id, user_id, bet):
    await ctx.message.edit_text(
                          _("👊 <i>Выберите действие</i>").format(
                              game_id,
                              bet
                              ),
                        parse_mode="HTML",
                        reply_markup=await get_rps_button(game_id))
    
    await asyncio.sleep(3)

@rps_router.callback_query(F.data.endswith("_rps_choose_button"))
async def choose_rps(ctx: types.CallbackQuery):
    choose = int(ctx.data.split("_")[1])
    game_id = int(ctx.data.split("_")[0])
    
    bank_id = await game_db.get_creator_id(game_id)
    
    player_choose = await rps_db.get_choose(game_id, "player")
    
    if player_choose != 0:
        await rps_db.add_choose(game_id, choose, "bank")
        
        player_id = await game_db.get_player_id(game_id)
        
        win_id, reason = await calculate_win(game_id, player_id, bank_id)
        
        await play_game.end_game(game_id, bank_id, player_id, win_id, reason)
        
        return
    
    await rps_db.add_choose(game_id, choose, "player")
    
    await dp.send_message(bank_id, _("👊 <i>Выберите действие и узнайте результат битвы</i>"),
                        parse_mode="HTML",
                        reply_markup=await get_rps_button(game_id))
    
    await ctx.message.edit_text(
                          _("👊 <i>Ваш выбор сделан, ждите соперника</i>"),
                        parse_mode="HTML",
                        reply_markup=await get_game_cancel_button())

async def calculate_win(game_id, player_id, bank_id):
    player_choose = await rps_db.get_choose(game_id, "player") - 1
    bank_choose = await rps_db.get_choose(game_id, "bank") - 1
    
    player_emoji = get_rps_object(player_choose)
    bank_emoji = get_rps_object(bank_choose)
    
    if player_choose == bank_choose:
        return None, _("{} Ничья").format(player_emoji)
    elif (player_choose - bank_choose + 3) % 3 == 1:
        await rps_db.add_score(game_id, 1, "bank")
        return bank_id, _("{}/{}").format(bank_emoji, player_emoji)
    else:
        await rps_db.add_score(game_id, 1, "player")
        return player_id, _("{}/{}").format(player_emoji, bank_emoji)

def get_rps_object(id):
    match id:
        case 0:
            return "✊"
        case 1:
            return "🖐"
        case 2:
            return "✌️"