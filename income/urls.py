from django.urls import path

from .views import IncomeCreateAPIView, IncomeRetrieveAPIView


urlpatterns = [
    path('income/create/', IncomeCreateAPIView.as_view(), name='income'),
    path('income/retrieve/<int:pk>/', IncomeRetrieveAPIView.as_view(), name='income-retrieve'),
]
