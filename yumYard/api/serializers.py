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
    followers = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('avatar', 'followers_count', 'followers', 'following_count', 'following', "username")

    def get_following_count(self, obj):
        return obj.user.following.count()

    def get_following(self, obj):
        return [profile.user.username for profile in obj.user.following.all()]

    def get_followers(self, obj):
        return [user.username for user in obj.followers.all()]


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
