from django.contrib import auth
from django.forms import ValidationError

from .models import Expense
from authentication.models import User

from rest_framework import serializers


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount']
