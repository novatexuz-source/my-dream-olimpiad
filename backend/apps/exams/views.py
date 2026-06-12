import html
import logging
import os

import requests
from django.utils import timezone
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from apps.registration.models import Participant
from apps.tests_app.models import Test, Question
from apps.exams.models import ExamSession, ExamAnswer
from apps.results.models import Result
from apps.exams.serializers import ExamSessionSerializer
import datetime

logger = logging.getLogger(__name__)


class ExamLoginThrottle(AnonRateThrottle):
    scope = 'exam_login'


def _send_result_notification(session):
    """Push the final score to the Telegram chat that registered this student.

    Fired once per session (when its Result row is first created) so neither
    the explicit finish endpoint nor the auto-expiry paths can double-send.
    """
    from apps.registration.views import _resolve_chat_id

    chat_id = _resolve_chat_id(session.participant.telegram_id)
    bot_token = os.getenv('BOT_TOKEN')
    if not chat_id or not bot_token:
        return

    text = (
        f"🏁 <b>Test yakunlandi!</b>\n\n"
        f"👤 <b>{html.escape(session.participant.full_name)}</b>\n"
        f"📚 {html.escape(session.test.subject.name)} — {html.escape(session.test.title)} ({session.test.grade}-sinf)\n\n"
        f"✅ To'g'ri javoblar: <b>{session.correct_count} ta</b>\n"
        f"❌ Xato/javobsiz: <b>{session.wrong_count} ta</b>\n"
        f"📊 Natija: <b>{session.percentage:.0f}%</b>\n"
        f"🏆 Ball: <b>{session.score}</b>"
    )
    try:
        requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "reply_markup": {
                    "inline_keyboard": [[
                        {"text": "📋 Javoblar tafsiloti", "callback_data": f"res_{session.id}"}
                    ]]
                },
            },
            timeout=8,
        )
    except Exception:
        logger.exception("Failed to send result notification for session %s", session.id)


def _finalize_session(session, finished_at=None):
    """Mark a session completed and compute its score from saved answers.

    Single source of truth for scoring — used by auto-expiry checks and the
    explicit finish endpoint.
    """
    test = session.test
    with transaction.atomic():
        session.status = 'completed'
        session.finished_at = finished_at or (
            session.started_at + datetime.timedelta(minutes=test.duration_minutes)
        )
        answers = ExamAnswer.objects.filter(session=session)
        correct = answers.filter(is_correct=True).count()
        total = test.questions.count()
        session.correct_count = correct
        session.wrong_count = total - correct
        session.total_questions = total
        session.percentage = (correct / total * 100) if total > 0 else 0
        session.score = correct * 10  # 10 points per question
        session.save()

        result, result_created = Result.objects.get_or_create(
            session=session,
            defaults={
                'participant': session.participant,
                'percentage': session.percentage,
            }
        )
        if result_created:
            transaction.on_commit(lambda: _send_result_notification(session))


def _get_session_for_code(session_id, unique_code):
    """Return (session, error_response). The caller must supply the
    participant's unique_code — session ids alone are not proof of identity.
    """
    if not unique_code:
        return None, Response({'error': "Unikal kod kiritilishi shart!"}, status=status.HTTP_403_FORBIDDEN)
    try:
        session = ExamSession.objects.select_related('participant', 'test').get(id=session_id)
    except ExamSession.DoesNotExist:
        return None, Response({'error': "Sessiya topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
    if session.participant.unique_code != str(unique_code):
        return None, Response({'error': "Unikal kod mos kelmadi!"}, status=status.HTTP_403_FORBIDDEN)
    return session, None


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ExamLoginThrottle])
def exam_login(request):
    unique_code = request.data.get('unique_code')
    if not unique_code:
        return Response({'error': "Unikal kodni kiriting!"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        participant = Participant.objects.get(unique_code=unique_code)
    except Participant.DoesNotExist:
        return Response({'error': "Bunday unikal kod topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

    if participant.verification_status != 'approved':
        return Response({'error': f"Sizning arizangiz holati: {participant.get_verification_status_display()}. Faqat tasdiqlangan ishtirokchilar test topshira oladi!"}, status=status.HTTP_400_BAD_REQUEST)

    # Parse subjects
    subjects_list = [s.strip() for s in participant.subject.split(',') if s.strip()]
    if not subjects_list:
        subjects_list = [participant.subject.strip()]

    # Find active/matching tests
    tests = Test.objects.filter(
        subject__name__in=subjects_list,
        grade=participant.grade,
        is_active=True
    ).select_related('subject')

    now = timezone.now()
    tests_data = []

    for t in tests:
        # Check if session exists
        session = ExamSession.objects.filter(participant=participant, test=t).first()

        session_status = 'not_started'
        session_id = None
        remaining_seconds = 0

        if session:
            session_id = str(session.id)
            # Auto-expire if in_progress but time limit exceeded
            if session.status == 'in_progress':
                elapsed = (now - session.started_at).total_seconds()
                limit = t.duration_minutes * 60
                if elapsed >= limit:
                    _finalize_session(session)
                    session_status = 'completed'
                else:
                    session_status = 'in_progress'
                    remaining_seconds = int(limit - elapsed)
            else:
                session_status = session.status
        else:
            # Check test start/end constraints
            if t.start_datetime and now < t.start_datetime:
                session_status = 'waiting_start'
            elif t.end_datetime and now > t.end_datetime:
                session_status = 'expired'
            else:
                session_status = 'available'

        tests_data.append({
            'id': str(t.id),
            'title': t.title,
            'subject_name': t.subject.name,
            'duration_minutes': t.duration_minutes,
            'start_datetime': t.start_datetime,
            'end_datetime': t.end_datetime,
            'status': session_status,
            'session_id': session_id,
            'remaining_seconds': remaining_seconds,
            'questions_count': t.questions.count()
        })

    return Response({
        'participant': {
            'id': str(participant.id),
            'full_name': participant.full_name,
            'grade': participant.grade,
            'unique_code': participant.unique_code
        },
        'tests': tests_data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_exam_session(request, session_id):
    session, error = _get_session_for_code(session_id, request.query_params.get('code'))
    if error:
        return error

    now = timezone.now()
    limit = session.test.duration_minutes * 60
    elapsed = (now - session.started_at).total_seconds()

    if session.status == 'in_progress' and elapsed >= limit:
        _finalize_session(session)

    serializer = ExamSessionSerializer(session)

    # Calculate exact remaining seconds for the countdown
    remaining_seconds = 0
    if session.status == 'in_progress':
        remaining_seconds = max(0, int(limit - elapsed))

    return Response({
        'session': serializer.data,
        'remaining_seconds': remaining_seconds
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def start_exam(request):
    participant_id = request.data.get('participant_id')
    test_id = request.data.get('test_id')
    unique_code = request.data.get('unique_code')

    if not participant_id or not test_id:
        return Response({'error': "participant_id va test_id kiritilishi shart!"}, status=status.HTTP_400_BAD_REQUEST)
    if not unique_code:
        return Response({'error': "Unikal kod kiritilishi shart!"}, status=status.HTTP_403_FORBIDDEN)

    try:
        participant = Participant.objects.get(id=participant_id)
        test = Test.objects.get(id=test_id)
    except (Participant.DoesNotExist, Test.DoesNotExist):
        return Response({'error': "Ishtirokchi yoki test topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

    # Identity + eligibility checks: code must match and participant approved
    if participant.unique_code != str(unique_code):
        return Response({'error': "Unikal kod mos kelmadi!"}, status=status.HTTP_403_FORBIDDEN)
    if participant.verification_status != 'approved':
        return Response({'error': "Faqat tasdiqlangan ishtirokchilar test topshira oladi!"}, status=status.HTTP_403_FORBIDDEN)

    # Check if a session already exists
    session = ExamSession.objects.filter(participant=participant, test=test).first()
    now = timezone.now()

    if session:
        if session.status == 'completed':
            return Response({'error': "Siz ushbu testni topshirib bo'lgansiz!"}, status=status.HTTP_400_BAD_REQUEST)
        elif session.status == 'in_progress':
            # Check if time exceeded
            elapsed = (now - session.started_at).total_seconds()
            limit = test.duration_minutes * 60
            if elapsed >= limit:
                _finalize_session(session)
                return Response({'error': "Sizning test topshirish vaqtingiz tugagan!"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ExamSessionSerializer(session)
            return Response(serializer.data)

    # Validate test window before starting a new session
    if not test.is_active:
        return Response({'error': "Test faol emas!"}, status=status.HTTP_400_BAD_REQUEST)
    if test.start_datetime and now < test.start_datetime:
        return Response({'error': "Test hali boshlanmadi!"}, status=status.HTTP_400_BAD_REQUEST)
    if test.end_datetime and now > test.end_datetime:
        return Response({'error': "Test topshirish vaqti tugagan!"}, status=status.HTTP_400_BAD_REQUEST)

    # Create new session
    session = ExamSession.objects.create(
        participant=participant,
        test=test,
        status='in_progress',
        started_at=now,
        total_questions=test.questions.count()
    )

    serializer = ExamSessionSerializer(session)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_answer(request):
    session_id = request.data.get('session_id')
    question_id = request.data.get('question_id')
    selected_answer = request.data.get('selected_answer')

    if not session_id or not question_id or not selected_answer:
        return Response({'error': "Barcha maydonlar to'ldirilishi shart!"}, status=status.HTTP_400_BAD_REQUEST)

    session, error = _get_session_for_code(session_id, request.data.get('unique_code'))
    if error:
        return error

    try:
        question = Question.objects.get(id=question_id, test=session.test)
    except Question.DoesNotExist:
        return Response({'error': "Savol topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

    if selected_answer not in ('A', 'B', 'C', 'D'):
        return Response({'error': "Javob A, B, C yoki D bo'lishi kerak!"}, status=status.HTTP_400_BAD_REQUEST)

    if session.status != 'in_progress':
        return Response({'error': "Sessiya faol emas!"}, status=status.HTTP_400_BAD_REQUEST)

    # Check time limit
    now = timezone.now()
    elapsed = (now - session.started_at).total_seconds()
    limit = session.test.duration_minutes * 60
    if elapsed >= limit:
        _finalize_session(session)
        return Response({'error': "Test vaqti tugadi!"}, status=status.HTTP_400_BAD_REQUEST)

    is_correct = (question.correct_answer == selected_answer)

    # Save or update answer
    ExamAnswer.objects.update_or_create(
        session=session,
        question=question,
        defaults={
            'selected_answer': selected_answer,
            'is_correct': is_correct,
            'answered_at': now
        }
    )

    return Response({'success': True})


@api_view(['POST'])
@permission_classes([AllowAny])
def finish_exam(request):
    session_id = request.data.get('session_id')

    if not session_id:
        return Response({'error': "Sessiya ID kiritilishi shart!"}, status=status.HTTP_400_BAD_REQUEST)

    session, error = _get_session_for_code(session_id, request.data.get('unique_code'))
    if error:
        return error

    if session.status == 'completed':
        # Already finished, just return status
        return Response({'success': True, 'already_finished': True})

    _finalize_session(session, finished_at=timezone.now())

    return Response({
        'success': True,
        'correct_count': session.correct_count,
        'wrong_count': session.wrong_count,
        'percentage': session.percentage,
        'score': session.score
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_exam_result(request, session_id):
    session, error = _get_session_for_code(session_id, request.query_params.get('code'))
    if error:
        return error

    if session.status != 'completed':
        return Response({'error': "Test hali yakunlanmagan!"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'participant_name': session.participant.full_name,
        'test_title': session.test.title,
        'subject_name': session.test.subject.name,
        'grade': session.test.grade,
        'correct_count': session.correct_count,
        'wrong_count': session.wrong_count,
        'total_questions': session.total_questions,
        'percentage': session.percentage,
        'score': session.score,
        'started_at': session.started_at,
        'finished_at': session.finished_at
    })
