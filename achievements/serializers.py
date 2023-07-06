from rest_framework import serializers
from .models import Achievement


class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = ['owner_id', 'date', 'description', 'amount', 'source']