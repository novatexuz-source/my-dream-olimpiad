from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Prefetch
from apps.results.models import Result
from apps.registration.models import Participant
from apps.exams.models import ExamSession


class ResultsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = ExamSession.objects.filter(
            status='completed'
        ).select_related(
            'participant', 'test', 'test__subject'
        ).order_by('-percentage', '-score', 'finished_at')

        # Optional filters
        search = request.query_params.get('search', '').strip()
        subject = request.query_params.get('subject', '').strip()
        grade = request.query_params.get('grade', '').strip()

        if search:
            sessions = sessions.filter(participant__full_name__icontains=search)
        if subject:
            sessions = sessions.filter(test__subject__name__iexact=subject)
        if grade:
            sessions = sessions.filter(test__grade=grade)

        cert_map = dict(
            Result.objects.filter(session__in=sessions)
            .values_list('session_id', 'certificate_sent')
        )

        data = []
        for idx, session in enumerate(sessions, start=1):
            data.append({
                'id': str(session.id),
                'rank': idx,
                'full_name': session.participant.full_name,
                'phone': session.participant.phone,
                'grade': session.test.grade,
                'subject': session.test.subject.name,
                'test_title': session.test.title,
                'correct_count': session.correct_count,
                'wrong_count': session.wrong_count,
                'total_questions': session.total_questions,
                'percentage': round(session.percentage, 1),
                'score': session.score,
                'finished_at': session.finished_at,
                'certificate_sent': cert_map.get(session.id, False),
            })

        return Response({
            'count': len(data),
            'results': data
        })


class AttendanceListView(APIView):
    """Public monitor: which registered students entered the test and which did not.

    Sensitive fields (unique_code, phone) are intentionally NOT exposed.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        participants = (
            Participant.objects
            .exclude(unique_code__isnull=True)
            .exclude(unique_code='')
            .prefetch_related(
                Prefetch(
                    'exam_sessions',
                    queryset=ExamSession.objects.order_by('-started_at'),
                )
            )
            .order_by('grade', 'full_name')
        )

        search = request.query_params.get('search', '').strip()
        subject = request.query_params.get('subject', '').strip()
        grade = request.query_params.get('grade', '').strip()
        status_f = request.query_params.get('status', '').strip()

        if search:
            participants = participants.filter(full_name__icontains=search)
        if subject:
            participants = participants.filter(subject__iexact=subject)
        if grade:
            participants = participants.filter(grade=grade)

        data = []
        entered_count = 0
        for p in participants:
            sessions = list(p.exam_sessions.all())
            completed = [s for s in sessions if s.status == 'completed']
            in_progress = [s for s in sessions if s.status == 'in_progress']
            entered = len(sessions) > 0
            if entered:
                entered_count += 1
            if completed:
                st, latest = 'completed', completed[0]
            elif in_progress:
                st, latest = 'in_progress', in_progress[0]
            elif sessions:
                st, latest = 'started', sessions[0]
            else:
                st, latest = 'not_entered', None
            is_done = st == 'completed' and latest is not None
            data.append({
                'id': str(p.id),
                'full_name': p.full_name,
                'grade': p.grade,
                'subject': p.subject,
                'entered': entered,
                'status': st,
                'percentage': round(latest.percentage, 1) if is_done else None,
                'score': latest.score if is_done else None,
                'started_at': latest.started_at if latest else None,
                'finished_at': latest.finished_at if latest else None,
            })

        total = len(data)
        not_entered_count = total - entered_count

        if status_f == 'entered':
            data = [d for d in data if d['entered']]
        elif status_f == 'not_entered':
            data = [d for d in data if not d['entered']]

        return Response({
            'count': len(data),
            'total': total,
            'entered_count': entered_count,
            'not_entered_count': not_entered_count,
            'results': data,
        })


class CertificateToggleView(APIView):
    """Toggle whether a participant's certificate has been issued."""
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = ExamSession.objects.select_related('participant').get(
                id=session_id, status='completed'
            )
        except ExamSession.DoesNotExist:
            return Response({'error': 'Sessiya topilmadi'}, status=404)

        result, _ = Result.objects.get_or_create(
            session=session,
            defaults={
                'participant': session.participant,
                'percentage': session.percentage,
            },
        )
        result.certificate_sent = not result.certificate_sent
        result.save(update_fields=['certificate_sent'])
        return Response({
            'success': True,
            'certificate_sent': result.certificate_sent,
        })
