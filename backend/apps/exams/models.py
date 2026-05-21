from django.db import models
import uuid
from apps.registration.models import Participant
from apps.tests_app.models import Test, Question

class ExamSession(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'Kutmoqda'),
        ('in_progress', 'Jarayonda'),
        ('completed', 'Tugatilgan'),
        ('expired', 'Muddati o\'tgan'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='exam_sessions')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='exam_sessions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    correct_count = models.IntegerField(default=0)
    wrong_count = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.participant.full_name} - {self.test.title}"

class ExamAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, null=True, blank=True, choices=(
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ))
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session.participant.full_name} - {self.question.order_number}"
