from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.validated_data
        return Response(user_data, status=status.HTTP_201_CREATED)
