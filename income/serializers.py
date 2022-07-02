from .models import Income

from rest_framework import serializers


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['__str__', 'source', 'description', 'amount']
