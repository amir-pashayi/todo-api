from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.serializers import UserSerializer


class UserRegisterApiView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class UserDetailApiView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        if 'password' in serializer.data:
            password = self.request.data.get('password')
            self.request.user.set_password(password)
            self.request.user.save()
        serializer.save()

