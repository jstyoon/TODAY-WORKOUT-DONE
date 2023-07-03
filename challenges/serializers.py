from rest_framework import serializers
from .models import Challenge



class ChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Challenge
        fields = ['id', 'date', 'description', 'amount', 'category']