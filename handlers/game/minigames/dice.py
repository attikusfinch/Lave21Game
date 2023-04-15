from keyboard.main_button import *
from database.game_db import Game, Dice, Poker
from create_bot import _
from aiogram import Router

from database.wallet_db import Wallet
from database.stats_db import Stats, GlobalStats

from keyboard.cancel_button import *

from create_bot import dp

import asyncio
from handlers.game import play_game

dice_router = Router()

game_db = Game()
dice_db = Dice()

wallet_db = Wallet()
stats_db = Stats()
global_stats_db = GlobalStats()

async def dice_game(ctx, game_id, user_id, bet):
    bank_id = int(await game_db.get_creator_id(game_id))

    bank_dice = await dp.send_dice(bank_id)
    player_dice = await dp.send_dice(user_id)

    await ctx.message.edit_text(
                          _("👊 <i>Вы кинули кубики <b>№ {}</b>" + 
                          " на сумму {} LAVE, через 3 секунды, они решат вышу судьбу</i>").format(
                              game_id,
                              bet
                              ),
                        parse_mode="HTML")

    await dp.send_message(bank_id,
                          _("👊 @{} <i>Вы кинули кубики <b>№ {}</b>" + 
                          " на сумму {} LAVE, через 3 секунды, они решат вышу судьбу</i>").format(
                              ctx.from_user.username,
                              game_id,
                              bet
                              ),
                            parse_mode="HTML")
    
    await asyncio.sleep(3)
    
    await dice_db.add_score(game_id, bank_dice.dice.value, "bank")
    await dice_db.add_score(game_id, player_dice.dice.value, "player")

    if bank_dice.dice.value < player_dice.dice.value:
        await play_game.end_game(game_id, bank_id, user_id, user_id, _("Удача"))
        return
    
    await play_game.end_game(game_id, bank_id, user_id, bank_id, _("Удача"))
