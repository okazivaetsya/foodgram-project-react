from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    RecipesViewSet, IngredientsViewSet,
    TagsViewSet, UsersViewSet)


app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
