from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    info = models.TextField(blank=True, null=True)
    favorites = models.ManyToManyField('Recipe', related_name='favorited_by', blank=True)

    def __str__(self):
        return self.user.username

    @property
    def followers_count(self):
        return self.followers.count()


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)

    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name='user', related_name='recipes', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipe_img/', null=True, blank=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return ratings.aggregate(models.Avg('rating'))['rating__avg']
        return None


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='ratings', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}: {self.rating}'


class Comment(models.Model):
    content = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name
