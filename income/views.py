from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Income
from .permissions import IsOwner
from .serializers import IncomeSerializer

# Create your views here.


class IncomeListAPIView(ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class IncomeDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner,
    ]
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(owner=user)
