from django.urls import path

from .views import IncomeCreateAPIView, IncomeRetrieveAPIView


urlpatterns = [
    path('create/', IncomeCreateAPIView.as_view(), name='income'),
    path('retrieve/<int:pk>/', IncomeRetrieveAPIView.as_view(), name='income-retrieve'),
]
