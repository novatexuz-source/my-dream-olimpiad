from django.contrib import admin
from .models import Participant, Payment, Operator

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'phone')

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'grade', 'subject', 'payment_type', 'payment_status', 'verification_status', 'operator', 'self_referral', 'unique_code', 'registered_at')
    list_filter = ('verification_status', 'payment_status', 'payment_type', 'grade', 'subject', 'operator', 'self_referral')
    search_fields = ('full_name', 'phone', 'unique_code')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('participant', 'type', 'amount', 'status', 'paid_at')
    list_filter = ('status', 'type')
    search_fields = ('participant__full_name', 'participant__phone')
