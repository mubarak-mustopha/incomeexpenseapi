from django.urls import path


from .views import ExpenseCategoryAPIView, IncomeCategoryAPIView

urlpatterns = [
    path("expense-data/", ExpenseCategoryAPIView.as_view()),
    path("income-data/", IncomeCategoryAPIView.as_view()),
]
