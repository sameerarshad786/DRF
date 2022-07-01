from django.urls import path

from .views import ExpenseCreateAPIView, ExpenseRetrieveAPIView


urlpatterns = [
    path('create/', ExpenseCreateAPIView.as_view(), name='expense'),
    path('retrieve/<int:pk>/', ExpenseRetrieveAPIView.as_view(), name='expense-retrieve'),
]