from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.results.models import Result
from apps.exams.models import ExamSession


class ResultsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = ExamSession.objects.filter(
            status='completed'
        ).select_related(
            'participant', 'test', 'test__subject'
        ).order_by('-finished_at')

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

        data = []
        for idx, session in enumerate(sessions, start=1):
            data.append({
                'id': str(session.id),
                'rank': idx,
                'full_name': session.participant.full_name,
                'phone': session.participant.phone_number,
                'grade': session.test.grade,
                'subject': session.test.subject.name,
                'test_title': session.test.title,
                'correct_count': session.correct_count,
                'wrong_count': session.wrong_count,
                'total_questions': session.total_questions,
                'percentage': round(session.percentage, 1),
                'score': session.score,
                'finished_at': session.finished_at,
            })

        return Response({
            'count': len(data),
            'results': data
        })
