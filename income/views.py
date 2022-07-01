from .serializers import IncomeSerializer
from .models import Income
from .permissions import IsOwner

from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend


class IncomeCreateAPIView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Income.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('id', 'owner', 'amount', 'source',)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class IncomeRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Income.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
