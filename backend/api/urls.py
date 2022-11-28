from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RecipesViewSet


app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
