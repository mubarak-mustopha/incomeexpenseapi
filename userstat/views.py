from django.db.models import Sum
from django.shortcuts import render


from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


from expenses.models import Expense
from income.models import Income

# Create your views here.
# expense_category_data
# income_sources_data
# {
#   "category_data": {
#     "OTHERS": {
#       "amount": "300.00"
#     },
#     "ONLINE_SERVICES": {
#       "amount": "789.00"
#     }
#   }
# }


class ExpenseCategoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(owner=request.user)
        expenses_category_sum = (
            expenses.order_by("category")
            .values("category")
            .annotate(cat_sum=Sum("amount"))
        )

        # category_data = {"ONLINE_SERVICE": {"amount": "23000"},"OTHERS": {"amount": "34000"},....}
        category_data = {
            category["category"]: {"amount": category["cat_sum"]}
            for category in expenses_category_sum
        }
        return Response({"category_data": category_data}, status=status.HTTP_200_OK)


class IncomeCategoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        income = Income.objects.filter(owner=request.user)
        income_sources_total = (
            income.order_by("source")
            .values("source")
            .annotate(source_total=Sum("amount"))
        )

        # category_data = {"ONLINE_SERVICE": {"amount": "23000"},"OTHERS": {"amount": "34000"},....}
        sources_data = {
            source["source"]: {"amount": source["source_total"]}
            for source in income_sources_total
        }
        return Response({"sources_data": sources_data}, status=status.HTTP_200_OK)
