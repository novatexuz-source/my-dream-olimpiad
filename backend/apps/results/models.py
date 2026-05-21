from django.db import models
import uuid
from apps.registration.models import Participant
from apps.exams.models import ExamSession

class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.OneToOneField(ExamSession, on_delete=models.CASCADE, related_name='result')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='results')
    rank = models.IntegerField(null=True, blank=True)
    place = models.CharField(max_length=20, choices=(
        ('1', '1-o\'rin'),
        ('2', '2-o\'rin'),
        ('3', '3-o\'rin'),
        ('none', 'O\'rinsiz'),
    ), default='none')
    percentage = models.FloatField(default=0.0)
    certificate_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant.full_name} - {self.place}"
