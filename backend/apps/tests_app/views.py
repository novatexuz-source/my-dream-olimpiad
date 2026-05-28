from datetime import datetime, date as date_cls
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Subject, Test
from .serializers import SubjectSerializer, TestSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny] # Change to IsAuthenticated later if needed

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all().order_by('-created_at')
    serializer_class = TestSerializer
    permission_classes = [permissions.AllowAny] # Change to IsAuthenticated later if needed

    @action(detail=False, methods=['post'], url_path='reschedule')
    def reschedule(self, request):
        """Move all tests + participants from one olympiad date to a new
        date/time. Optionally overrides start/end time for all tests.
        Body: {
          "from_date": "YYYY-MM-DD",
          "to_date": "YYYY-MM-DD",
          "start_time": "HH:MM:SS"   (optional — applied to ALL tests),
          "end_time":   "HH:MM:SS"   (optional — applied to ALL tests)
        }
        If start_time/end_time omitted, time-of-day on each test is preserved.
        """
        from apps.registration.models import Participant
        from django.utils.timezone import make_aware

        from_date_str = request.data.get('from_date')
        to_date_str = request.data.get('to_date')
        start_time_str = request.data.get('start_time')
        end_time_str = request.data.get('end_time')

        if not from_date_str or not to_date_str:
            return Response(
                {'error': "from_date va to_date kerak"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': "Sana noto'g'ri formatda (YYYY-MM-DD bo'lishi kerak)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        def parse_hms(s):
            for fmt in ('%H:%M:%S', '%H:%M'):
                try:
                    t = datetime.strptime(s, fmt).time()
                    return t
                except ValueError:
                    continue
            return None

        start_time = parse_hms(start_time_str) if start_time_str else None
        end_time = parse_hms(end_time_str) if end_time_str else None

        if from_date == to_date and not start_time and not end_time:
            return Response({'updated_tests': 0, 'updated_participants': 0, 'note': 'O\'zgarish yo\'q'})

        # Don't allow moving to a date that's already taken by other tests
        if to_date != from_date and Test.objects.filter(start_datetime__date=to_date).exists():
            return Response(
                {'error': f"{to_date.strftime('%d.%m.%Y')} sanasida allaqachon testlar bor"},
                status=status.HTTP_400_BAD_REQUEST
            )

        affected_tests = Test.objects.filter(start_datetime__date=from_date)
        if not affected_tests.exists():
            return Response(
                {'error': f"{from_date.strftime('%d.%m.%Y')} sanasida testlar topilmadi"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            tests_count = 0
            for test in affected_tests:
                if test.start_datetime:
                    new_start = test.start_datetime.replace(
                        year=to_date.year, month=to_date.month, day=to_date.day
                    )
                    if start_time:
                        new_start = new_start.replace(
                            hour=start_time.hour,
                            minute=start_time.minute,
                            second=start_time.second,
                            microsecond=0,
                        )
                    test.start_datetime = new_start
                if test.end_datetime:
                    new_end = test.end_datetime.replace(
                        year=to_date.year, month=to_date.month, day=to_date.day
                    )
                    if end_time:
                        new_end = new_end.replace(
                            hour=end_time.hour,
                            minute=end_time.minute,
                            second=end_time.second,
                            microsecond=0,
                        )
                    test.end_datetime = new_end
                test.save()
                tests_count += 1

            # Move participants whose target_test_date matches
            participants_count = Participant.objects.filter(
                target_test_date=from_date
            ).update(target_test_date=to_date)

            # Also sync any orphans (NULL or pointing to non-existent dates)
            from .serializers import sync_approved_participants_to_upcoming_date
            extra = sync_approved_participants_to_upcoming_date(to_date)

        return Response({
            'updated_tests': tests_count,
            'updated_participants': participants_count + extra,
            'from_date': from_date_str,
            'to_date': to_date_str,
        })
