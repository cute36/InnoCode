from aiogram.fsm.state import State,StatesGroup

class Download(StatesGroup):
    wait_link=State()
    wait_format=State()
    wait_file=State()

class ID(StatesGroup):
    wait_id = State()