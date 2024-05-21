from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)

    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.name
