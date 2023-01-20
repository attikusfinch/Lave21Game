from aiogram import Router
from keyboard.main_button import *
from create_bot import _
from aiogram import F, Router
from settings import WALLET
from keyboard.withdraw_button import get_deposit_buttons

start_deposit_router = Router()

@start_deposit_router.callback_query(F.data == "deposit_button")
async def deposit(ctx):
    user_id = ctx.from_user.id
    
    await ctx.message.edit_text(
        _("📥 Используйте адрес ниже для пополнения баланса." + "\n" + "\n" +

        "Монета: Lavandos, (LAVE) или TON" + "\n" + 
        "Сеть: The Open Network – TON" + "\n" +
        "Коментарий: <code>{}</code>" + "\n" + "\n" +

        "<code>{}</code>" + "\n" + "\n" + 
        
        "<b>ЧТОБЫ ВАШИ СРЕДСТВА ПОПАЛИ НА ВАШ БАЛАНС ВАМ НУЖНО ОБЯЗАТЕЛЬНО " + 
        "ВВЕСТИ КОМЕНТАРИЙ К ПЛАТЕЖУ, ИНАЧЕ ОНИ БУДУТ НАВСЕГДА УТЕРЯНЫ. " + 
        "ТАКЖЕ АДМИНИСТРАЦИЯ НЕ НЕСЕТ НИКАКОЙ ОТВЕТСТВЕННОСТИ ПРИ НЕ УКАЗАНИИ ПАРОЛЯ " +
        "И/ИЛИ ПЕРЕВОДОВ С ДРУГИХ КОШЕЛЬКОВ КРОМЕ TONKEEPER. "
        "И ПОМНИТЕ, КРИПТОВАЛЮТА TONCOIN НЕ ИСПОЛЬЗУЕТСЯ В БОТЕ, А НУЖНА ЧТОБ ОПЛАТИТЬ " + 
        "КОМИССИЮ ПРИ ВЫВОДЕ ВАШИХ СРЕДСТВ.</b>").format(user_id, WALLET),
        parse_mode="HTML",
        reply_markup=await get_deposit_buttons(user_id)
        )