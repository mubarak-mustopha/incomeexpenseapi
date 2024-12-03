from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Expense
from .permissions import IsOwner
from .serializers import ExpenseSerializer

# Create your views here.


class ExpenseListAPIView(ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner,
    ]
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(owner=user)
