import random
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
        """Return questions in a per-student shuffled order, each with its
        options shuffled too. The shuffle is seeded by the session id (and the
        question id for options), so it stays stable across reloads/resume but
        differs from student to student. Each option keeps its original letter
        ('key') so grading (comparing to Question.correct_answer) is unchanged.
        """
        questions = list(obj.test.questions.all())
        random.Random(str(obj.id)).shuffle(questions)

        result = []
        for q in questions:
            options = [
                {'key': 'A', 'text': q.option_a},
                {'key': 'B', 'text': q.option_b},
                {'key': 'C', 'text': q.option_c},
                {'key': 'D', 'text': q.option_d},
            ]
            random.Random(f"{obj.id}:{q.id}").shuffle(options)
            result.append({
                'id': str(q.id),
                'order_number': q.order_number,
                'question_text': q.question_text,
                'question_image': q.question_image,
                'options': options,
                # Kept for backward compatibility during deploy transition.
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d,
            })
        return result

    def get_answers(self, obj):
        answers = obj.answers.all()
        return ExamAnswerSerializer(answers, many=True).data
