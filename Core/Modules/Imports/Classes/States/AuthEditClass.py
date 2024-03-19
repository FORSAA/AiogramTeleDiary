from aiogram.fsm.state import StatesGroup, State


class AuthEdit(StatesGroup):
    changing_login = State()
    changing_password = State()