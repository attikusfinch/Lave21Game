from typing import NamedTuple

from aiogram.types import BotCommand

class _BaseCommands(NamedTuple):
    START: BotCommand = BotCommand(command="start", description="Запуск бота")
    SETTINGS: BotCommand = BotCommand(command="settings", description="Настойки бота")
    TIP: BotCommand = BotCommand(command="tip", description="Перевести LAVE")

BaseCommands = _BaseCommands()