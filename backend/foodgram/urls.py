from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from recipe.views import RecipeViewSet
from tags.views import TagViewSet
from user.views import UserViewSet
from django.contrib import admin
from django.urls import path, include

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'recipes', RecipeViewSet, basename='recipe')
router_v1.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router_v1.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
