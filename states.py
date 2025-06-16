from aiogram.fsm.state import State,StatesGroup

class Download(StatesGroup):
    wait_link=State()
    wait_format=State()
    wait_file=State()

class ID(StatesGroup):
    wait_id = State()

class Sticker(StatesGroup):
    waiting_for_sticker = State()
class Photo(StatesGroup):
    waiting_for_photo = State()