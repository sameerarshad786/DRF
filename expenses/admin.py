from django.contrib import admin

from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['owner', 'category', 'description', 'amount', 'whenpublished']
    list_filter = ['owner', 'amount', 'created_at']

admin.site.register(Expense, ExpenseAdmin)