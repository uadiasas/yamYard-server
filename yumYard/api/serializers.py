from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import UserProfile, Recipe, Comment


class UserSerializer(serializers.ModelSerializer):
    recipes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'recipes', 'comments']


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = ('avatar', 'followers_count')


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'content', 'user', 'comments', 'category']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'recipe']
