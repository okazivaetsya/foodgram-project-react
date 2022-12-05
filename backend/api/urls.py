from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TagsViewSet, RecipesViewSet, IngredientsViewSet

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
