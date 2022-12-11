from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (CreateUserView, FavoriteViewSet, FollowViewSet,
                    IngredientsViewSet, RecipesViewSet, ShoppingCartViewSet,
                    TagsViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('users', CreateUserView, basename='users')

urlpatterns = [
    path(
        'users/subscriptions/',
        FollowViewSet.as_view({'get': 'list'}),
        name='subscriptions'
    ),
    path(
        'users/<user_id>/subscribe/',
        FollowViewSet.as_view({'post': 'create', 'delete': 'delete'}),
        name='subscribe'
    ),
    path(
        'recipes/<recipe_id>/favorite/',
        FavoriteViewSet.as_view({'post': 'create', 'delete': 'delete'}),
        name='favorite'
    ),
    path(
        'recipes/<recipe_id>/shopping_cart/',
        ShoppingCartViewSet.as_view({'post': 'create', 'delete': 'delete'}),
        name='shopping_cart'
    ),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
