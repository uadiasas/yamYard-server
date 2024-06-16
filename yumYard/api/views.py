from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

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



class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_to_follow = get_object_or_404(UserProfile, user__username=kwargs['username'])
        if request.user.profile != user_to_follow:
            user_to_follow.followers.add(request.user)
            return Response({'status': 'subscribed'}, status=status.HTTP_200_OK)
        return Response({'status': 'cannot subscribe to yourself'}, status=status.HTTP_400_BAD_REQUEST)

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_to_unfollow = get_object_or_404(UserProfile, user__username=kwargs['username'])
        if request.user.profile != user_to_unfollow:
            user_to_unfollow.followers.remove(request.user)
            return Response({'status': 'unsubscribed'}, status=status.HTTP_200_OK)
        return Response({'status': 'cannot unsubscribe from yourself'}, status=status.HTTP_400_BAD_REQUEST)


class AddToFavoritesAPIView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_profile = self.request.user.profile
        recipe_id = request.data.get('recipe_id')
        if not recipe_id:
            return Response({"detail": "Recipe ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return Response({"detail": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

        user_profile.favorites.add(recipe)
        user_profile.save()
        return Response({"detail": "Recipe added to favorites."}, status=status.HTTP_200_OK)


class RemoveFromFavoritesAPIView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_profile = self.request.user.profile
        recipe_id = request.data.get('recipe_id')
        if not recipe_id:
            return Response({"detail": "Recipe ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return Response({"detail": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

        user_profile.favorites.remove(recipe)
        user_profile.save()
        return Response({"detail": "Recipe removed from favorites."}, status=status.HTTP_200_OK)
