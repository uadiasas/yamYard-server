from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Recipe)
