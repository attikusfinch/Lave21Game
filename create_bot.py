from aiogram import Bot, Dispatcher
import settings
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.middlewares.language_middleware import setup_middleware

from aiogram.utils.i18n import gettext

API_TOKEN = settings.TOKEN

storage = MemoryStorage()
dp = Bot(token=API_TOKEN)
bot = Dispatcher(bot=dp, storage=storage)

i18n = setup_middleware(bot)
_ = gettext