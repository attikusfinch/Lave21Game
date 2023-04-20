from keyboard.main_button import *
from database.game_db import Game, Dice, Poker, Rps
from create_bot import _
from aiogram import Router, F, types

from database.wallet_db import Wallet
from database.stats_db import Stats, GlobalStats

from keyboard.game_button import get_game_button
from keyboard.cancel_button import *

from create_bot import dp

from handlers.game.minigames.dice import dice_game
from handlers.game.minigames.poker import card_game
from handlers.game.minigames.rps import rps_game

main_game_menu_router = Router()

game_db = Game()
dice_db = Dice()
poker_db = Poker()
rps_db = Rps()

wallet_db = Wallet()
stats_db = Stats()
global_stats_db = GlobalStats()

@main_game_menu_router.callback_query(F.data.endswith("_start_game_button"))
async def start_game(ctx: types.CallbackQuery):
    user_id = ctx.from_user.id
    game_id = int(ctx.data.split("_")[0])
    
    game_checker = await game_db.check_game(game_id)
    
    if game_checker is False:
        await ctx.message.edit_text(_("❕ Ошибка, игра уже идет, выберите другую игру или создайте новую."),
                                    reply_markup=await get_game_button(user_id))
        return

    balance = await wallet_db.get_lave(user_id)
    bet = await game_db.get_bet(game_id)

    if balance < bet:
        await ctx.message.edit_text(_("❕ Ошибка, на вашем балансе недостаточно LAVE."),
                                    reply_markup=await get_game_button(user_id))
        return
    
    await wallet_db.set_lave(user_id, bet, False)

    game_type = await game_db.get_game_type(game_id)
    
    await game_db.add_player(game_id, user_id)
    
    if game_type == 1: # add game types
        await card_game(ctx, game_id, user_id, bet)
    elif game_type == 2:
        await dice_game(ctx, game_id, user_id, bet)
    elif game_type == 3:
        await rps_game(ctx, game_id, user_id, bet)

async def end_game(game_id, bank_id, player_id, win_id, reason):
    bank_username = (await dp.get_chat(bank_id)).username
    player_username = (await dp.get_chat(player_id)).username   
    
    game_type = await game_db.get_game_type(game_id)

    if game_type == 1:
        bank_score = await poker_db.get_score(game_id)
        player_score = await poker_db.get_score(game_id, "player")
    elif game_type == 2:
        bank_score = await dice_db.get_score(game_id)
        player_score = await dice_db.get_score(game_id, "player")
    elif game_type == 3:
        bank_score = await rps_db.get_score(game_id)
        player_score = await rps_db.get_score(game_id, "player")
    
    bet = await game_db.get_bet(game_id)
    
    bet = await fee(bet, 1) # add fee 1%

    msg = _(
        "<b>🕹 Результат игры №</b> {}:" + "\n" +
        "╠ @{} - {}  ⚔️ @{} - {}" + "\n" +
        "║ <b>Победитель:</b>  @{} [{}]" + "\n" +
        "╚ <b>Cумма выигрыша:</b>  <code>{}</code> LAVE"
    ).format(
        game_id,
        bank_username,
        bank_score, 
        player_username,
        player_score,
        player_username if win_id == player_id else bank_username,
        reason,
        bet
    )

    if win_id is not None:
        bank_win = (bank_id == win_id)

        await stats_db.update_stats(player_id, (not bank_win))
        await stats_db.update_stats(bank_id, bank_win)

        await wallet_db.set_lave(win_id, bet*2)
    else:
        await wallet_db.set_lave(player_id, bet)
        await wallet_db.set_lave(bank_id, bet)

    await global_stats_db.set_game_count()
    await global_stats_db.set_lave_count(bet)

    await game_db.delete_game(game_id)
    
    if game_type == 1:
        await poker_db.delete_game(game_id)
    elif game_type == 2:
        await dice_db.delete_game(game_id)
    elif game_type == 3:
        await rps_db.delete_game(game_id)

    await dp.send_message(bank_id, msg, parse_mode="HTML", reply_markup=await get_game_button(bank_id))
    await dp.send_message(player_id, msg, parse_mode="HTML", reply_markup=await get_game_button(player_id))

async def fee(bet, percent):
    return round(bet*((100-percent)/100))