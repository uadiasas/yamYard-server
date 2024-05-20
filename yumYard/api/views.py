from rest_framework import generics
from . import serializers
from django.contrib.auth.models import User

from .serializers import UserProfileSerializer


class UserAPIList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserAPIDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile