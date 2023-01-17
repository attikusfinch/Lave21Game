from keyboard.main_button import *
from database.game_db import Game
from create_bot import _
from aiogram import Router, F, types

from database.wallet_db import Wallet
from database.stats_db import Stats, GlobalStats

from keyboard.cancel_button import *

from create_bot import dp

from keyboard.game_button import get_game_button, get_gaming_button, get_banking_button

from handlers.constants import cards

import random

start_play_game_router = Router()

game_db = Game()
wallet_db = Wallet()
stats_db = Stats()
global_stats_db = GlobalStats()

@start_play_game_router.callback_query(F.data.endswith("_start_game_button"))
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
    
    bank_score = await get_card()
    player_score = await get_card()

    checker = await game_db.add_player(game_id, user_id) # двойная проверка, если всё будет работать, надо вырезать

    if checker is False:
        await ctx.message.edit_text(_("❕ Ошибка, игра уже идет, выберите другую игру или создайте новую."),
                                    reply_markup=await get_game_button(user_id))
        return
    
    bank_id = int(await game_db.get_bank_id(game_id))

    await game_db.add_score(game_id, bank_score)
    await game_db.add_score(game_id, player_score, "player")
    
    await game_db.set_banking(False, game_id)
    
    await ctx.message.edit_text(
                          _("👌 <i>Вы успешно присоединились к игре <b>№ {}</b>" + 
                          " на сумму {} LAVE</i>").format(
                              game_id,
                              bet
                              ),
                        parse_mode="HTML")
    
    await dp.send_message(bank_id, 
                          _("👌 @{} <i>присоединился к игре <b>№ {}</b>" + 
                          " на сумму {} LAVE , ожидайте свой ход.</i>").format(
                              ctx.from_user.username,
                              game_id,
                              bet
                              ),
                            parse_mode="HTML")
    
    await send_score(user_id, 1, player_score, await get_gaming_button(game_id))

async def send_card(player_id, user_id):
    """
        Объясню. Тут мы должны идти от обратного, так как карта отправляется нашему противнику, то и условие:
        Если player, то bank_id и если bank, то player_id
    """
    user = (await dp.get_chat(user_id))
    
    await dp.send_message(player_id, _("🃏 @{} взял(а) карту.").format(user.username))

@start_play_game_router.callback_query(F.data.endswith("_pass_button"))
async def pass_game(ctx: types.CallbackQuery):
    game_id = ctx.data.split("_")[0]
    user_id = ctx.from_user.id
    
    game_status = await game_db.get_game(game_id)
    
    if game_status is None:
        await ctx.message.edit_text(_("❕ Ошибка, игра уже закончилась."), get_game_button(user_id))
    
    await game_db.set_banking(True, game_id)
    
    player_count = await game_db.get_step(game_id, "player")
    bank_id = await game_db.get_bank_id(game_id)
    
    bank_username = (await dp.get_chat(bank_id)).username
    
    await ctx.message.edit_text(
        _("✅ Вы закончили игру, теперь играет @{}, ожидайте результат.").format(bank_username), 
        reply_markup=await get_game_cancel_button()
        )
    
    await dp.send_message(bank_id, 
                          _("✔️ @{} закончил играть и у него {} карт, банкуй").format(
                              ctx.from_user.username, 
                              player_count)
    )
    
    bank_count = await game_db.get_step(game_id, "bank")
    bank_score = await game_db.get_score(game_id, "bank")
    
    await send_score(bank_id, bank_count, bank_score, await get_banking_button(game_id))

@start_play_game_router.callback_query(F.data.endswith("_add_card_button"))
async def play_game(ctx: types.CallbackQuery):
    game_id = ctx.data.split("_")[0]
    
    user_id = ctx.from_user.id
    
    game_exist = await game_db.get_game(game_id)
    
    if game_exist is None:
        await ctx.answer(_("Игра закончена"))
        return

    player_id = await game_db.get_player_id(game_id)
    bank_id = await game_db.get_bank_id(game_id)
    banking = await game_db.get_banking(game_id)

    markup = await get_gaming_button(game_id)
    
    # Проверка на банкира
    if banking and bank_id != user_id:
        await ctx.answer(_("Сейчас ходит банк, ждите"))
        return
    
    score = await get_card()
    
    player = "bank" if bank_id == user_id else "player"

    await game_db.add_score(game_id, score, player)
    
    if banking:
        markup = await get_banking_button(game_id)

    await send_card(player_id if banking else bank_id, bank_id if banking else player_id)
    
    player_score = await game_db.get_score(game_id, player)
    player_count = await game_db.get_step(game_id, player)

    win_id = player_id if player == "player" else bank_id

    if player_count == 2 and player_score == 22:
        await ctx.message.delete()
        await end_game(game_id, bank_id, player_id, win_id, _("Набрал золотой сет"))
        return
    
    if player_score == 21:
        await ctx.message.delete()
        await end_game(game_id, bank_id, player_id, win_id, _("Набрал 21"))
        return

    if player_score > 21:
        win_id = player_id if player != "player" else bank_id
        await ctx.message.delete()
        await end_game(game_id, bank_id, player_id, win_id, _("Перебор очков"))
        return
    
    await show_score(ctx, player_count, player_score, markup)

@start_play_game_router.callback_query(F.data.endswith("_end_game_button"))
async def close_game(ctx: types.CallbackQuery):
    game_id = ctx.data.split("_")[0]
    
    bank_id = await game_db.get_bank_id(game_id)
    player_id = await game_db.get_player_id(game_id)

    if bank_id is None or player_id is None:
        await ctx.answer(_("Игра закончена"))
        return

    bank_score = await game_db.get_score(game_id, "bank")
    player_score = await game_db.get_score(game_id, "player")
    
    win_id = bank_id if bank_score >= player_score else player_id
    
    await end_game(game_id, bank_id, player_id, win_id, "Результат игры")

async def get_card():
    return random.choice(cards)

async def show_score(ctx, card_count, user_score, markup):
    await ctx.message.edit_text(
        _("ℹ️ Количество карт: {}" + "\n" + "\n" +
        
        "🔄 Количество очков: {}").format(
            card_count,
            user_score            
        ), reply_markup=markup)

async def send_score(user_id, card_count, user_score, markup):
    await dp.send_message(user_id,
        _("ℹ️ Количество карт: {}" + "\n" + "\n" +
        
        "🔄 Количество очков: {}").format(
            card_count,
            user_score            
        ), reply_markup=markup)

async def end_game(game_id, bank_id, player_id, win_id, reason):
    bank_username = (await dp.get_chat(bank_id)).username
    player_username = (await dp.get_chat(player_id)).username   
    
    bank_score = await game_db.get_score(game_id)
    player_score = await game_db.get_score(game_id, "player")
    
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

    bank_win = (bank_id == win_id)

    await stats_db.update_stats(player_id, (not bank_win))
    await stats_db.update_stats(bank_id, bank_win)

    await wallet_db.set_lave(win_id, bet*2)
    
    await global_stats_db.set_game_count()
    await global_stats_db.set_lave_count(bet)

    await game_db.delete_game(game_id)

    await dp.send_message(bank_id, msg, parse_mode="HTML", reply_markup=await get_game_button(bank_id))
    await dp.send_message(player_id, msg, parse_mode="HTML", reply_markup=await get_game_button(player_id))

async def fee(bet, percent):
    return round(bet*((100-percent)/100))