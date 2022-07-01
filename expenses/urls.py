from django.urls import path

from .views import ExpenseCreateAPIView, ExpenseRetrieveAPIView


urlpatterns = [
    path('expense/create/', ExpenseCreateAPIView.as_view(), name='expense'),
    path('expense/retrieve/<int:pk>/', ExpenseRetrieveAPIView.as_view(), name='expense-retrieve'),
]