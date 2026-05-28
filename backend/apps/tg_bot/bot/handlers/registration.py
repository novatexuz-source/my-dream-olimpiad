from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from apps.tg_bot.bot.states.registration import RegistrationState
from apps.tg_bot.bot.keyboards.reply import get_grades_keyboard, get_subjects_keyboard, get_payment_types_keyboard, get_phone_keyboard, get_confirm_keyboard, get_edit_fields_keyboard
from apps.tests_app.models import Subject
from asgiref.sync import sync_to_async

router = Router()

# URL of your registration form (HTTPS via Cloudflare Tunnel)
WEBAPP_URL = "https://sherman-contributions-treasurer-concerts.trycloudflare.com/register"

async def show_confirmation(message: Message, state: FSMContext):
    data = await state.get_data()
    text = (
        f"📝 <b>Iltimos, ma'lumotlaringizni tekshiring!</b>\n\n"
        f"⚠️ Bu ma'lumotlar sertifikatda xuddi shunday tartibda chiqadi:\n\n"
        f"👤 <b>Ism:</b> {data.get('first_name', '')}\n"
        f"👤 <b>Familiya:</b> {data.get('last_name', '')}\n"
        f"🏫 <b>Sinf:</b> {data.get('grade', '')}-sinf\n"
        f"📚 <b>Fan:</b> {data.get('subject', '')}\n"
        f"📱 <b>Telefon:</b> {data.get('phone', '')}\n"
        f"💳 <b>To'lov turi:</b> {str(data.get('payment_type', '')).capitalize()}\n"
    )
    await message.answer(text, reply_markup=get_confirm_keyboard(), parse_mode="HTML")
    await state.set_state(RegistrationState.confirm)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    
    from apps.registration.models import Participant
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
    
    telegram_id = f"tg_{message.from_user.id}"
    
    @sync_to_async
    def has_profiles():
        return Participant.objects.filter(telegram_id=telegram_id).exists()
        
    exists = await has_profiles()
    
    if exists:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👥 Profillar"), KeyboardButton(text="📝 Yangi profil qo'shish")]
            ],
            resize_keyboard=True
        )
        
        await message.answer(
            "🏆 <b>My Dream International Olimpiad</b>\n\n"
            "Xush kelibsiz! Quyidagi menyudan kerakli bo'limni tanlang:\n"
            "Bitta akkauntdan bir nechta o'quvchilarni ro'yxatdan o'tkazishingiz mumkin.",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="📝 Ro'yxatdan o'tish",
                web_app=WebAppInfo(url=f"{WEBAPP_URL}?action=new")
            )]
        ])
        msg = await message.answer(
            "🏆 <b>My Dream International Olimpiad</b>\n\n"
            "Xush kelibsiz! Olimpiadaga ro'yxatdan o'tish uchun quyidagi tugmani bosing:\n\n"
            "📌 <i>Ro'yxatdan o'tgandan so'ng operatorlarimiz siz bilan bog'lanadilar.</i>",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        _save_temp_msg_id(message.from_user.id, msg.message_id)

@router.message(F.text == "📝 Yangi profil qo'shish")
async def show_new_student_btn(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📝 Ro'yxatdan o'tish",
            web_app=WebAppInfo(url=f"{WEBAPP_URL}?action=new")
        )]
    ])
    msg = await message.answer(
        "Yangi profil qo'shish uchun quyidagi tugmani bosing:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    _save_temp_msg_id(message.from_user.id, msg.message_id)

import json
import os
def _save_temp_msg_id(tg_id, msg_id):
    cache_file = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'temp_msg_cache.json')
    data = {}
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
        except Exception:
            pass
    data[str(tg_id)] = msg_id
    try:
        with open(cache_file, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass

@router.message(F.text == "👥 Profillar")
async def show_profiles(message: Message, state: FSMContext):
    from apps.registration.models import Participant
    telegram_id = f"tg_{message.from_user.id}"
    
    @sync_to_async
    def get_participants():
        return list(Participant.objects.filter(telegram_id=telegram_id).order_by('-registered_at'))
        
    participants = await get_participants()
    
    if not participants:
        await message.answer("Sizda hali ro'yxatdan o'tgan o'quvchilar yo'q. 'Yangi profil qo'shish' tugmasini bosing.")
        return
    
    
    for participant in participants:
        status_emoji = {'pending': '⏳', 'approved': '✅', 'rejected': '❌'}.get(participant.verification_status, '⏳')
        status_text = {'pending': 'Tekshirilmoqda', 'approved': 'Tasdiqlangan', 'rejected': 'Rad etilgan'}.get(participant.verification_status, 'Kutilmoqda')
        
        text = (
            f"👤 <b>F.I.O:</b> {participant.full_name}\n"
            f"🏫 <b>Sinf:</b> {participant.grade}-sinf\n"
            f"📚 <b>Fan:</b> {participant.subject}\n"
            f"📱 <b>Telefon:</b> {participant.phone}\n"
            f"{status_emoji} <b>Holati:</b> {status_text}"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="✏️ Tahrirlash",
                web_app=WebAppInfo(url=f"{WEBAPP_URL}?id={participant.id}")
            )],
            [InlineKeyboardButton(
                text="🗑 O'chirish",
                callback_data=f"del_prof_{participant.id}"
            )]
        ])
        
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

from aiogram.types import CallbackQuery

@router.callback_query(F.data.startswith("del_prof_"))
async def process_delete_profile(callback: CallbackQuery):
    participant_id = callback.data.replace("del_prof_", "")
    from apps.registration.models import Participant
    
    @sync_to_async
    def delete_participant():
        try:
            p = Participant.objects.get(id=participant_id)
            # Only allow deleting own profiles
            if p.telegram_id == f"tg_{callback.from_user.id}":
                p.delete()
                return True
        except Participant.DoesNotExist:
            pass
        return False
        
    success = await delete_participant()
    if success:
        await callback.message.edit_text("✅ Profil o'chirildi.")
        import asyncio
        await asyncio.sleep(2)
        try:
            await callback.message.delete()
        except Exception:
            pass
    else:
        await callback.answer("Profil topilmadi yoki o'chirishga ruxsat yo'q.", show_alert=True)
    
    await callback.answer()




@router.message(RegistrationState.first_name)
async def process_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Familiyangizni kiriting:")
    await state.set_state(RegistrationState.last_name)

@router.message(RegistrationState.last_name)
async def process_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Sinfingizni tanlang:", reply_markup=get_grades_keyboard())
    await state.set_state(RegistrationState.grade)

@router.message(RegistrationState.grade)
async def process_grade(message: Message, state: FSMContext):
    grade_str = message.text.replace("-sinf", "")
    if not grade_str.isdigit():
        await message.answer("Iltimos, tugmalardan foydalaning.")
        return
    await state.update_data(grade=int(grade_str))
    
    # Get subjects from DB
    subjects = await sync_to_async(list)(Subject.objects.filter(is_active=True).values_list('name', flat=True))
    if not subjects:
        subjects = ["Matematika", "Ingliz tili", "Rus tili"] # Default fallback
        
    await message.answer("Fanni tanlang:", reply_markup=get_subjects_keyboard(subjects))
    await state.set_state(RegistrationState.subject)

@router.message(RegistrationState.subject)
async def process_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=get_phone_keyboard())
    await state.set_state(RegistrationState.phone)

@router.message(RegistrationState.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)
    await message.answer("To'lov turini tanlang (190,000 so'm):", reply_markup=get_payment_types_keyboard())
    await state.set_state(RegistrationState.payment_type)

@router.message(RegistrationState.payment_type)
async def process_payment_type(message: Message, state: FSMContext):
    payment_type = message.text.lower()
    await state.update_data(payment_type=payment_type)
    await show_confirmation(message, state)

@router.message(RegistrationState.confirm)
async def process_confirm(message: Message, state: FSMContext):
    from aiogram.types import ReplyKeyboardRemove
    
    if message.text == "✏️ Tahrirlash":
        await message.answer("Qaysi ma'lumotni tahrirlamoqchisiz?", reply_markup=get_edit_fields_keyboard())
        await state.set_state(RegistrationState.edit_field)
        return
        
    if message.text != "✅ Tasdiqlash":
        await message.answer("Iltimos, quyidagi tugmalardan birini tanlang.")
        return

    data = await state.get_data()
    from apps.registration.models import Participant, Payment
    
    if data['payment_type'] == "click":
        await message.answer("Click orqali to'lov uchun link: [CLICK LINK]\nTo'lov qilganingizdan so'ng tasdiqlanadi.", reply_markup=ReplyKeyboardRemove())
    elif data['payment_type'] == "payme":
        await message.answer("Payme orqali to'lov uchun link: [PAYME LINK]\nTo'lov qilganingizdan so'ng tasdiqlanadi.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Naqd to'lov uchun ofisimizga tashrif buyuring yoki karta raqamiga tashlang: 8600...", reply_markup=ReplyKeyboardRemove())
    
    @sync_to_async
    def create_participant():
        from apps.registration.views import get_next_olympiad_date
        full_name = f"{data['last_name']} {data['first_name']}"
        defaults = {
            'full_name': full_name,
            'phone': data['phone'],
            'grade': data['grade'],
            'subject': data['subject'],
            'payment_type': data['payment_type'],
        }
        # Only auto-assign target_test_date for NEW participants (don't overwrite existing)
        existing = Participant.objects.filter(telegram_id=str(message.from_user.id)).first()
        if not existing:
            defaults['target_test_date'] = get_next_olympiad_date()
        participant, created = Participant.objects.update_or_create(
            telegram_id=str(message.from_user.id),
            defaults=defaults
        )
        
        payment, p_created = Payment.objects.get_or_create(
            participant=participant,
            defaults={
                'type': data['payment_type'],
                'amount': 190000.00
            }
        )
        if not p_created:
            payment.type = data['payment_type']
            payment.save()
            
        return participant
        
    try:
        await create_participant()
        await message.answer("Ma'lumotlaringiz qabul qilindi. Operatorlarimiz tekshirib, tasdiqlaganidan so'ng sizga 6 xonali maxsus kod yuboriladi.\n\n⚠️ Diqqat: Test kuni o'zingiz bilan pasport yoki tug'ilganlik haqidagi guvohnomangizni olib kelishni unutmang!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        await message.answer(f"Xatolik yuz berdi: {str(e)}")
        
    await state.clear()

@router.message(RegistrationState.edit_field)
async def process_edit_field(message: Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        await show_confirmation(message, state)
        return
        
    valid_fields = ["Ism", "Familiya", "Sinf", "Fan", "Telefon", "To'lov turi"]
    if message.text not in valid_fields:
        await message.answer("Iltimos, quyidagi tugmalardan birini tanlang.")
        return
        
    await state.update_data(editing_field=message.text)
    
    from aiogram.types import ReplyKeyboardRemove
    if message.text == "Sinf":
        await message.answer("Yangi sinfingizni tanlang:", reply_markup=get_grades_keyboard())
    elif message.text == "Fan":
        subjects = ["Matematika", "Ingliz tili", "Rus tili"]
        await message.answer("Yangi fanni tanlang:", reply_markup=get_subjects_keyboard(subjects))
    elif message.text == "To'lov turi":
        await message.answer("Yangi to'lov turini tanlang:", reply_markup=get_payment_types_keyboard())
    elif message.text == "Telefon":
        await message.answer("Yangi telefon raqamingizni yuboring:", reply_markup=get_phone_keyboard())
    else:
        await message.answer(f"Yangi {message.text.lower()}ni kiriting:", reply_markup=ReplyKeyboardRemove())
        
    await state.set_state(RegistrationState.edit_value)

@router.message(RegistrationState.edit_value)
async def process_edit_value(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get('editing_field')
    
    if field == "Ism":
        await state.update_data(first_name=message.text)
    elif field == "Familiya":
        await state.update_data(last_name=message.text)
    elif field == "Sinf":
        grade_str = message.text.replace("-sinf", "")
        if not grade_str.isdigit():
            await message.answer("Iltimos, tugmalardan foydalaning.")
            return
        await state.update_data(grade=int(grade_str))
    elif field == "Fan":
        await state.update_data(subject=message.text)
    elif field == "Telefon":
        phone = message.contact.phone_number if message.contact else message.text
        await state.update_data(phone=phone)
    elif field == "To'lov turi":
        await state.update_data(payment_type=message.text.lower())
        
    # Return to confirmation
    await show_confirmation(message, state)

