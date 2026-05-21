from rest_framework import serializers
from apps.exams.models import ExamSession, ExamAnswer
from apps.tests_app.models import Question, Test
from apps.registration.models import Participant

class ExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 
            'order_number', 
            'question_text', 
            'question_image', 
            'option_a', 
            'option_b', 
            'option_c', 
            'option_d'
        ]

class ExamAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAnswer
        fields = ['id', 'question', 'selected_answer']

class ExamSessionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    participant_name = serializers.CharField(source='participant.full_name', read_only=True)
    test_title = serializers.CharField(source='test.title', read_only=True)
    duration_minutes = serializers.IntegerField(source='test.duration_minutes', read_only=True)

    class Meta:
        model = ExamSession
        fields = [
            'id', 
            'participant', 
            'participant_name',
            'test', 
            'test_title',
            'status', 
            'started_at', 
            'finished_at', 
            'duration_minutes', 
            'questions', 
            'answers'
        ]

    def get_questions(self, obj):
        questions = obj.test.questions.all().order_by('order_number')
        return ExamQuestionSerializer(questions, many=True).data

    def get_answers(self, obj):
        answers = obj.answers.all()
        return ExamAnswerSerializer(answers, many=True).data
