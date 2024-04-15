from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('v1/users/', views.UserAPIList.as_view()),
    path('v1/users/<int:pk>/', views.UserAPIDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
