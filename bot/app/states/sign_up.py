from aiogram.fsm.state import State, StatesGroup

class UserSign(StatesGroup):
    fio =State()
    login=State()
    phone=State()
    password=State()
    birthday=State()
    gender=State()
    address=State()
    