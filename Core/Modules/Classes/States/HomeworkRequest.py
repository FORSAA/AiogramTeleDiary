from aiogram.fsm.state import StatesGroup, State


class HomeworkRequest(StatesGroup):
    selecting_wish_type = State()
    selecting_day = State()
