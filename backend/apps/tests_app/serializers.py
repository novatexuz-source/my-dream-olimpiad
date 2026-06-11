from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from .models import Subject, Test, Question


def sync_approved_participants_to_upcoming_date(target_date):
    """Move all approved participants whose target_test_date is NULL or
    points to a date with no tests, onto `target_date`.
    """
    from apps.registration.models import Participant
    valid_dates = set(
        Test.objects
        .exclude(start_datetime__isnull=True)
        .values_list('start_datetime__date', flat=True)
    )
    orphans = Participant.objects.filter(
        verification_status='approved'
    ).filter(
        Q(target_test_date__isnull=True) | ~Q(target_test_date__in=valid_dates)
    )
    return orphans.update(target_test_date=target_date)

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'order_number', 'question_text', 'question_image', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'subject', 'subject_name', 'grade', 'title', 'duration_minutes', 'passing_percentage', 'start_datetime', 'end_datetime', 'is_active', 'created_at', 'questions']

    def validate(self, data):
        subject = data.get('subject')
        grade = data.get('grade')
        start_datetime = data.get('start_datetime')

        if subject and grade and start_datetime:
            test_date = start_datetime.date()
            instance = self.instance

            existing = Test.objects.filter(
                subject=subject,
                grade=grade,
                start_datetime__date=test_date
            )
            if instance:
                existing = existing.exclude(pk=instance.pk)

            if existing.exists():
                raise serializers.ValidationError(
                    f"Bu fandan {grade}-sinf uchun {test_date.strftime('%d.%m.%Y')} kuni allaqachon test mavjud!"
                )

            # Only ONE future olympiad date allowed across all tests.
            today = timezone.localdate()
            if test_date >= today:
                other_future_dates = Test.objects.filter(
                    start_datetime__date__gte=today
                ).exclude(
                    start_datetime__date=test_date
                )
                if instance:
                    other_future_dates = other_future_dates.exclude(pk=instance.pk)
                if other_future_dates.exists():
                    existing_date = other_future_dates.first().start_datetime.date()
                    raise serializers.ValidationError(
                        f"Faqat bitta kelajakdagi olimpiada sanasi mumkin. "
                        f"Hozir {existing_date.strftime('%d.%m.%Y')} sanasiga rejalashtirilgan. "
                        f"Yangi sana qo'shish uchun avval uni o'chiring."
                    )

        return data

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        test = Test.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(test=test, **question_data)

        # If this is a future olympiad date, sync ALL orphaned approved
        # participants (NULL target OR pointing to a no-longer-existing date)
        # to this upcoming date.
        if test.start_datetime and test.start_datetime.date() >= timezone.localdate():
            sync_approved_participants_to_upcoming_date(test.start_datetime.date())

        return test

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', None)
        
        # Update test instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update questions if provided
        if questions_data is not None:
            # For simplicity, we delete old and recreate. A more robust way would check IDs.
            instance.questions.all().delete()
            for question_data in questions_data:
                Question.objects.create(test=instance, **question_data)
                
        return instance
