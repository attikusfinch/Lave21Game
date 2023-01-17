from aiogram.fsm.state import State, StatesGroup

class GameState(StatesGroup):
    get_game_type = State()
    get_lave_count = State()