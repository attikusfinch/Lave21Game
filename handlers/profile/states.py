from aiogram.fsm.state import State, StatesGroup

class WalletState(StatesGroup):
    get_wallet = State()

class WithdrawState(StatesGroup):
    get_amount = State()
    get_approve = State()