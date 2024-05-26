from rest_framework import generics, permissions
from . import serializers
from django.contrib.auth.models import User
from .models import Recipe, UserProfile
from .serializers import RecipeSerializer, UserProfileSerializer
from .permissions import IsOwnerOrReadOnly


class UserAPIList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserAPIDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class RecipeAPIList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeAPIDelete(generics.RetrieveDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

