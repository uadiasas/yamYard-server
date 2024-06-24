from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from . import serializers
from django.contrib.auth.models import User
from .models import Recipe, UserProfile, Category, Comment, Rating
from .serializers import RecipeSerializer, UserProfileSerializer, CategorySerializer, CommentSerializer, \
    RatingSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminUser, IsReadOnly

from .filters import RecipeFilter

#Пользователи
class UserAPIList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserAPIDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


#Рецепты
class RecipeAPIList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RecipeFilter
    search_fields = ['title', 'content', 'category__name']
    ordering_fields = ['title', 'time_created']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RecipeAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RecipeAPIDelete(generics.RetrieveDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


#Оценки
class RatingAPIList(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RatingAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

class RatingAPIDelete(generics.RetrieveDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]


class RateRecipe(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, recipe_id):
        user = request.user
        recipe = Recipe.objects.get(id=recipe_id)
        rating_value = request.data.get('rating')

        if not 1 <= int(rating_value) <= 5:
            return Response({"detail": "Rating must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)

        rating, created = Rating.objects.get_or_create(user=user, recipe=recipe, defaults={'rating': rating_value})

        if not created:
            rating.rating = rating_value
            rating.save()

        serializer = RatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, recipe_id):
        user = request.user
        recipe = Recipe.objects.get(id=recipe_id)
        rating_value = request.data.get('rating')

        if not 1 <= int(rating_value) <= 5:
            return Response({"detail": "Rating must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rating = Rating.objects.get(user=user, recipe=recipe)
            rating.rating = rating_value
            rating.save()
        except Rating.DoesNotExist:
            return Response({"detail": "Rating does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_200_OK)


#Профиль пользователя
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

#Категории
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


#Комментарии
class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)