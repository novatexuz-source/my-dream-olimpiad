from rest_framework import serializers
from .models import Participant, Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    class Meta:
        model = Participant
        fields = '__all__'
