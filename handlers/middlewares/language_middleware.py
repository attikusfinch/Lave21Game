from aiogram import types
from aiogram import Dispatcher

from aiogram.utils.i18n.core import I18n

from aiogram.utils.i18n.middleware import I18nMiddleware
from settings import I18N_DOMAIN, LOCALES_DIR, WORKDIR

from database.users_db import Users
from aiogram.types import TelegramObject

from typing import Dict, Any

async def get_lang(user_id: int):
    db = Users()
    
    return await db.get_language(user_id)

class ACLMiddleWare(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        user = types.User.get_current()

        if user is None:
            return "ru"

        lang = await get_lang(user.id)
        lang = lang if lang is not None else user.language_code
        return lang

def setup_middleware(bot: Dispatcher):
    i18n = I18n(path=LOCALES_DIR, default_locale="ru", domain=I18N_DOMAIN)
    i18n = ACLMiddleWare(i18n)
    
    i18n.setup(bot)
    
    return i18n