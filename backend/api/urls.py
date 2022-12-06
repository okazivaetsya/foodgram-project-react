from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import (
    TagsViewSet, RecipesViewSet,
    IngredientsViewSet, CreateUserView
)


app_name = 'api'

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('users', CreateUserView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
