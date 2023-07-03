from rest_framework import serializers
from .models import Prize



class PrizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prize
        fields = ['id', 'date', 'description', 'amount', 'source']