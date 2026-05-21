from django.db import models
import uuid

class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tests')
    grade = models.IntegerField(help_text="Sinf")
    title = models.CharField(max_length=255)
    duration_minutes = models.IntegerField(default=60)
    passing_percentage = models.FloatField(default=70.0)
    start_datetime = models.DateTimeField(null=True, blank=True, help_text="Test boshlanish vaqti")
    end_datetime = models.DateTimeField(null=True, blank=True, help_text="Test tugash vaqti")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.grade}-sinf)"

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    order_number = models.IntegerField(default=1)
    question_text = models.TextField()
    question_image = models.URLField(null=True, blank=True)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=(
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order_number']

    def __str__(self):
        return f"Savol {self.order_number}: {self.test.title}"
