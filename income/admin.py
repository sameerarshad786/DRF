from django.contrib import admin

from .models import Income


class IncomeAdmin(admin.ModelAdmin):
    list_display = ['owner', 'source', 'description', 'amount', 'whenpublished']
    list_filter = ['owner', 'amount', 'created_at']

admin.site.register(Income, IncomeAdmin)