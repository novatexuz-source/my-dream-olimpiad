from rest_framework import serializers
from .models import Subject, Test, Question

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
            # Check if a test for same subject+grade already exists on the same date
            test_date = start_datetime.date()
            existing = Test.objects.filter(
                subject=subject,
                grade=grade,
                start_datetime__date=test_date
            )
            # Exclude current instance if updating
            instance = self.instance
            if instance:
                existing = existing.exclude(pk=instance.pk)
            
            if existing.exists():
                raise serializers.ValidationError(
                    f"Bu fandan {grade}-sinf uchun {test_date.strftime('%d.%m.%Y')} kuni allaqachon test mavjud!"
                )
        
        return data

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        test = Test.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(test=test, **question_data)
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
