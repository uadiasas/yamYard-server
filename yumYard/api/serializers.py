from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import UserProfile, Recipe, Comment, Category


class UserSerializer(serializers.ModelSerializer):
    recipes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'recipes', 'comments']


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'content', 'user', 'comments', 'category']


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    followers = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    favorites = RecipeSerializer(many=True, read_only=True)
    info = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = UserProfile
        fields = ('avatar', 'followers_count', 'followers', 'following_count', 'following', "username",
                  'recipes_count', 'recipes', 'info', 'favorites')

    def get_following_count(self, obj):
        return obj.user.following.count()

    def get_following(self, obj):
        return [profile.user.username for profile in obj.user.following.all()]

    def get_followers(self, obj):
        return [user.username for user in obj.followers.all()]

    def get_recipes_count(self, obj):
        return obj.user.recipes.count()

    def get_recipes(self, obj):
        recipes = obj.user.recipes.all()
        return RecipeSerializer(recipes, many=True).data






class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'recipe']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image']