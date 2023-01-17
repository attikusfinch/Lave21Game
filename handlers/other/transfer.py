from keyboard.main_button import *
from database.game_db import Game
from create_bot import _
from aiogram import Router, F, types

from database.wallet_db import Wallet
from database.stats_db import Stats

from keyboard.cancel_button import *

from create_bot import dp

from keyboard.game_button import get_game_button, get_gaming_button, get_banking_button

from handlers.constants import cards

import random
from commands.bot_commands import BaseCommands

# ПОКА-ЧТО ПУСТЬ ЛЕЖИТ

start_tip_router = Router()

wallet_db = Wallet()

@dp.message_handler(BaseCommands.TIP)
async def tip(ctx: types.Message):
    # Get the command arguments
    user_id = ctx.from_user.id
    
    args = ctx.get_args().split()
    
    # Check if the user provided an amount
    if len(args) < 1:
        await ctx.reply("Введите количество для перевода")
        return
    
    # check if the ctx is a reply
    if ctx.reply_to_ctx is None:
        await ctx.reply("Для перевода, нужно ответить, на сообщение пользователя")
        return
    
    # Get the amount and the comment if provided
    amount = args[0]
    comment = " ".join(args[1:]) if len(args) > 1 else None
    
    # Get the ID of the user to send the coins to
    receiver_id = ctx.reply_to_ctx.from_user.id
    
    # Perform the database query to transfer the money
    #  ADD YOUR DATABASE QUERY HERE, use receiver_id as receiver
    wallet_db.set_lave(user_id, amount, False)
    wallet_db.set_lave(receiver_id, amount)
    
    # Confirm the transaction to the user
    if comment is not None:
        await ctx.reply(f"Successfully sent {amount} to user with ID {receiver_id} with comment: {comment}.")
    else:
        await ctx.reply(f"Successfully sent {amount} to user with ID {receiver_id}.")