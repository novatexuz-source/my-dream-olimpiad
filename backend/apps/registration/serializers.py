from rest_framework import serializers
from .models import Participant, Payment, Operator

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class OperatorSerializer(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Operator
        fields = ['id', 'name', 'phone', 'is_active', 'created_at', 'participants_count']

    def get_participants_count(self, obj):
        return obj.participants.count()

class ParticipantSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    operator_name = serializers.CharField(source='operator.name', read_only=True, default=None)
    class Meta:
        model = Participant
        fields = '__all__'
