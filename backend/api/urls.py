from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserView, IngredientsViewSet, RecipesViewSet,
                    TagsViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('users', CustomUserView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
