from .models import Expense

from rest_framework import serializers


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['__str__', 'id', 'category', 'description', 'amount']
