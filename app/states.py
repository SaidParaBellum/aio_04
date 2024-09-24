from aiogram.fsm.state import StatesGroup, State


class NoteState(StatesGroup):
    title = State()
    description = State()