from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_grades_keyboard():
    kb = [
        [KeyboardButton(text=f"{i}-sinf") for i in range(1, 4)],
        [KeyboardButton(text=f"{i}-sinf") for i in range(4, 7)],
        [KeyboardButton(text=f"{i}-sinf") for i in range(7, 10)],
        [KeyboardButton(text="10-sinf"), KeyboardButton(text="11-sinf")],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_subjects_keyboard(subjects):
    kb = [[KeyboardButton(text=subj)] for subj in subjects]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_payment_types_keyboard():
    kb = [
        [KeyboardButton(text="Click"), KeyboardButton(text="Payme")],
        [KeyboardButton(text="Naqd")],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_phone_keyboard():
    kb = [[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_confirm_keyboard():
    kb = [
        [KeyboardButton(text="✅ Tasdiqlash"), KeyboardButton(text="✏️ Tahrirlash")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_edit_fields_keyboard():
    kb = [
        [KeyboardButton(text="Ism"), KeyboardButton(text="Familiya")],
        [KeyboardButton(text="Sinf"), KeyboardButton(text="Fan")],
        [KeyboardButton(text="Telefon"), KeyboardButton(text="To'lov turi")],
        [KeyboardButton(text="🔙 Orqaga")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
