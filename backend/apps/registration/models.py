from django.db import models
import uuid

class Participant(models.Model):
    PAYMENT_CHOICES = (
        ('click', 'Click'),
        ('payme', 'Payme'),
        ('cash', 'Naqd'),
    )
    PAYMENT_STATUS = (
        ('pending', 'Kutilmoqda'),
        ('paid', 'To\'langan'),
        ('rejected', 'Rad etilgan'),
    )
    VERIFICATION_STATUS = (
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlangan'),
        ('rejected', 'Rad etilgan'),
    )
    CALL_STATUS = (
        ('new', 'Yangi'),
        ('no_answer', 'Ko\'tarmadi'),
        ('confirmed', 'Keladi'),
        ('declined', 'Rad etildi'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telegram_id = models.CharField(max_length=50)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    grade = models.IntegerField(help_text="1-11 sinf")
    subject = models.CharField(max_length=100) # Or ForeignKey to Subject model
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    call_status = models.CharField(max_length=20, choices=CALL_STATUS, default='new')
    unique_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    passport_or_birth_cert = models.URLField(null=True, blank=True, help_text="Supabase Image URL")
    rejection_reason = models.TextField(null=True, blank=True)
    target_test_date = models.DateField(null=True, blank=True, help_text="Qaysi olimpiada kunida qatnashadi")
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='payments')
    type = models.CharField(max_length=10, choices=Participant.PAYMENT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=190000.00)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Kutilmoqda'),
        ('confirmed', 'Tasdiqlangan'),
        ('rejected', 'Rad etilgan'),
    ), default='pending')
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.participant.full_name} - {self.amount}"
