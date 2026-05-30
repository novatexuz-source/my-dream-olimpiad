import random
import string
import requests
from datetime import date as date_cls
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from .models import Participant, Payment
from .serializers import ParticipantSerializer
from decouple import config


def _resolve_chat_id(telegram_id):
    """Return a numeric Telegram chat_id usable by the Bot API, or None.

    Stored telegram_id can be 'tg_12345' (web form), a raw '12345' (bot flow),
    or 'web_998...' (web user with no Telegram chat). Only the first two can
    receive messages.
    """
    if not telegram_id:
        return None
    tg_id = str(telegram_id)
    if tg_id.startswith('tg_'):
        return tg_id[3:]
    if tg_id.isdigit():
        return tg_id
    return None


def get_next_olympiad_date():
    """Return the next upcoming olympiad date (earliest future Test date) or None."""
    from apps.tests_app.models import Test
    today = date_cls.today()
    next_test = (
        Test.objects
        .filter(start_datetime__date__gte=today)
        .order_by('start_datetime')
        .first()
    )
    return next_test.start_datetime.date() if next_test and next_test.start_datetime else None

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all().order_by('-registered_at')
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        target_date = self.request.query_params.get('target_test_date')
        if target_date == 'null':
            qs = qs.filter(target_test_date__isnull=True)
        elif target_date:
            qs = qs.filter(target_test_date=target_date)
        return qs
    
    def generate_unique_code(self):
        while True:
            code = ''.join(random.choices(string.digits, k=6))
            if not Participant.objects.filter(unique_code=code).exists():
                return code

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        participant = self.get_object()
        
        if participant.verification_status == 'approved':
            return Response({'status': 'already approved'})
            
        code = self.generate_unique_code()
        participant.verification_status = 'approved'
        participant.payment_status = 'paid'
        participant.unique_code = code
        participant.save()

        # Send telegram message (strip the tg_ prefix so Telegram accepts the chat_id)
        real_tg_id = _resolve_chat_id(participant.telegram_id)
        if real_tg_id:
            BOT_TOKEN = config('BOT_TOKEN', default='')
            text = f"🎉 Tabriklaymiz! Arizangiz tasdiqlandi.\n\nSizning unikal kodingiz: <b>{code}</b>\n\nIltimos bu kodni saqlab qo'ying, test kuni kerak bo'ladi."
            try:
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    data={
                        "chat_id": real_tg_id,
                        "text": text,
                        "parse_mode": "HTML"
                    }
                )
            except Exception as e:
                print("Failed to send TG message", e)

        return Response({'status': 'approved', 'code': code})
        
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        participant = self.get_object()
        reason = request.data.get('reason', 'Noma\'lum sabab')
        
        participant.verification_status = 'rejected'
        participant.payment_status = 'rejected'
        participant.rejection_reason = reason
        participant.save()

        real_tg_id = _resolve_chat_id(participant.telegram_id)
        if real_tg_id:
            BOT_TOKEN = config('BOT_TOKEN', default='')
            text = f"❌ Kechirasiz, arizangiz rad etildi.\nSabab: {reason}"
            try:
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    data={
                        "chat_id": real_tg_id,
                        "text": text,
                        "parse_mode": "HTML"
                    }
                )
            except Exception:
                pass

        return Response({'status': 'rejected'})

    @action(detail=True, methods=['post'], url_path='call-status')
    def update_call_status(self, request, pk=None):
        participant = self.get_object()
        new_status = request.data.get('call_status')
        
        if new_status not in dict(Participant.CALL_STATUS):
            return Response(
                {'error': f"Noto'g'ri status: {new_status}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        participant.call_status = new_status
        participant.save()
        
        return Response({
            'status': 'updated',
            'call_status': new_status
        })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def public_register(request):
    """Public endpoint for web form registration (no auth required)"""
    data = request.data
    
    required = ['full_name', 'phone', 'grade', 'subject', 'payment_type']
    for field in required:
        if not data.get(field):
            return Response({'error': f'{field} maydoni to\'ldirilishi shart'}, status=status.HTTP_400_BAD_REQUEST)
    
    phone = data['phone'].replace(' ', '').replace('-', '')
    
    participant_id = data.get('id')
    participant = None
    created = False
    
    if participant_id:
        try:
            participant = Participant.objects.get(id=participant_id)
            participant.full_name = data['full_name']
            participant.phone = phone
            participant.grade = int(data['grade'])
            participant.subject = data['subject']
            participant.payment_type = data['payment_type']
            participant.save()
        except Participant.DoesNotExist:
            participant = None
            
    if not participant:
        participant = Participant.objects.create(
            telegram_id=data.get('telegram_id') or f'web_{phone}',
            full_name=data['full_name'],
            phone=phone,
            grade=int(data['grade']),
            subject=data['subject'],
            payment_type=data['payment_type'],
            target_test_date=get_next_olympiad_date(),
        )
        created = True
    
    
    subjects_list = data.get('subject', '').split(',')
    subjects_count = max(1, len([s.strip() for s in subjects_list if s.strip()]))
    calculated_amount = 190000.00 + (subjects_count - 1) * 90000.00
    
    payment, p_created = Payment.objects.get_or_create(
        participant=participant,
        defaults={'type': data['payment_type'], 'amount': calculated_amount}
    )
    if not p_created:
        payment.type = data['payment_type']
        payment.amount = calculated_amount
        payment.save()
    
    # Send confirmation message with Edit button via Telegram API
    if participant.telegram_id and participant.telegram_id.startswith('tg_'):
        real_tg_id = participant.telegram_id.replace('tg_', '')
        BOT_TOKEN = config('BOT_TOKEN', default='')
        
        status_emoji = '⏳'
        status_text = 'Tekshirilmoqda'
        
        payment_text = {
            'click': 'Click',
            'payme': 'Payme',
            'cash': 'Naqd pul'
        }.get(participant.payment_type, participant.payment_type)
        
        text = (
            f"🎉 <b>Tabriklaymiz, siz muvaffaqiyatli ro'yxatdan o'tdingiz!</b>\n\n"
            f"📋 <b>Sizning ma'lumotlaringiz:</b>\n\n"
            f"👤 <b>F.I.O:</b> {participant.full_name}\n"
            f"🏫 <b>Sinf:</b> {participant.grade}-sinf\n"
            f"📚 <b>Fan:</b> {participant.subject}\n"
            f"📱 <b>Telefon:</b> {participant.phone}\n"
            f"💳 <b>To'lov turi:</b> {payment_text} ({int(calculated_amount):,} so'm)\n\n"
            f"{status_emoji} <b>Holati:</b> {status_text}\n\n"
            f"<i>Ma'lumotlaringizda xato bo'lsa, quyidagi tugma orqali tahrirlashingiz mumkin.</i>"
        )
        
        WEBAPP_URL = "https://my-dream-olimpiad-4vdk.vercel.app/register"
        import json, os
        reply_markup = {
            "inline_keyboard": [
                [{"text": "✏️ Tahrirlash", "web_app": {"url": f"{WEBAPP_URL}?id={participant.id}"}}],
                [{"text": "🗑 O'chirish", "callback_data": f"del_prof_{participant.id}"}]
            ]
        }
        
        try:
            cache_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'temp_msg_cache.json')
            
            # Delete all previously tracked bot messages
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, 'r') as f:
                        cache_data = json.load(f)
                    old_msg_ids = cache_data.pop(str(real_tg_id), [])
                    if isinstance(old_msg_ids, int):
                        old_msg_ids = [old_msg_ids]
                    for old_id in old_msg_ids:
                        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage", json={
                            "chat_id": real_tg_id, "message_id": old_id
                        })
                    with open(cache_file, 'w') as f:
                        json.dump(cache_data, f)
                except Exception:
                    pass

            # Send confirmation message (with all inline buttons - no reply keyboard needed)
            conf_resp = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
                "chat_id": real_tg_id,
                "text": text,
                "reply_markup": reply_markup,
                "parse_mode": "HTML"
            }).json()
            
            # Track this message ID for cleanup next time
            if conf_resp.get("ok"):
                try:
                    existing = {}
                    if os.path.exists(cache_file):
                        with open(cache_file, 'r') as f:
                            existing = json.load(f)
                    existing[str(real_tg_id)] = [conf_resp["result"]["message_id"]]
                    with open(cache_file, 'w') as f:
                        json.dump(existing, f)
                except Exception:
                    pass
                    
        except Exception as e:
            print("Failed to send TG message on register", e)
    
    return Response({
        'success': True,
        'message': 'Arizangiz qabul qilindi! Operatorlarimiz tekshirib, tasdiqlaganidan so\'ng siz bilan bog\'lanamiz.',
        'id': str(participant.id)
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_by_id(request):
    participant_id = request.query_params.get('id')
    if not participant_id:
        return Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        participant = Participant.objects.get(id=participant_id)
        
        last_name = ''
        first_name = participant.full_name
        if ' ' in participant.full_name:
            parts = participant.full_name.split(' ', 1)
            last_name = parts[0]
            first_name = parts[1]
            
        return Response({
            'id': str(participant.id),
            'first_name': first_name,
            'last_name': last_name,
            'phone': participant.phone,
            'grade': participant.grade,
            'subjects': participant.subject.split(', ') if participant.subject else [],
            'payment_type': participant.payment_type
        })
    except Participant.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


