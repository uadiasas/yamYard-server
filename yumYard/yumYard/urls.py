from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView

from api.views import UserProfileDetailView, UserProfileUpdateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    #re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),  # Просмотр профиля
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
