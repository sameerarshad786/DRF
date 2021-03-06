from .serializers import ExpenseSerializer
from .models import Expense
from .permissions import IsOwner

from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

class ExpenseCreateAPIView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Expense.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('id', 'owner', 'amount', 'description', 'category',)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

class ExpenseRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Expense.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)