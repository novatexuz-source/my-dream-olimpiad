from aiogram.fsm.state import StatesGroup, State

class RegistrationState(StatesGroup):
    first_name = State()
    last_name = State()
    grade = State()
    subject = State()
    phone = State()
    payment_type = State()
    waiting_for_payment = State()
    waiting_for_document = State()
    confirm = State()
    edit_field = State()
    edit_value = State()
