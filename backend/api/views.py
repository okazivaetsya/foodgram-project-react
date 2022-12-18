from django.conf import settings
from django.db.models import Sum
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import CustomUser, Follow
from recipes.models import (
    Favorites, Ingredients, IngredientsInRecipes,
    Recipes, ShoppingCart, Tags
)
from .filters import IngredientsFilter, RecipeFilter
from .pagination import FoodgramPagination
from .serializers import (
    FavoriteSerializer, FollowSerializer,
    IngredientSerializer, RecipePostSerializer,
    RecipeSerializer, SimpleRecipeSerializer,
    TagsSerializer, UserSerializer
)
from .services import create_pdf


class TagsViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с тегами"""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с рецептами"""
    queryset = Recipes.objects.all()
    pagination_class = FoodgramPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipePostSerializer

    @staticmethod
    def _add_recipe_to(self, request, pk, model, my_serializer):
        recipe_id = pk
        if request.method == 'POST':
            recipe = get_object_or_404(Recipes, id=recipe_id)
            serializer = my_serializer(
                recipe, context={'request': request}
            )
            serializer.validate(serializer.data)
            model.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        user_id = request.user.id
        recipe = get_object_or_404(
            model, user__id=user_id,
            recipe__id=recipe_id
        )
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk):
        """Добавление и удаление рецепта в избранное"""
        return self._add_recipe_to(request, pk, Favorites, FavoriteSerializer)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """Добавление и удаление рецепта в список покупок"""
        return self._add_recipe_to(
            request, pk, ShoppingCart, SimpleRecipeSerializer
        )

    @action(detail=False)
    def download_shopping_cart(self, request):
        """Формирование и выгрузка pdf со списком покупок"""
        user = request.user
        ingredients = IngredientsInRecipes.objects.filter(
            recipe__shopping_cart__user=user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            sum_amount=Sum('amount')
        )
        return create_pdf(ingredients, settings.SHOPPING_LIST_FILE_NAME)


class IngredientsViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с ингредиентами"""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientsFilter


class CustomUserView(UserViewSet):
    """Вьюсет для работы с пользователями"""
    pagination_class = FoodgramPagination
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        pagination_class=FoodgramPagination
    )
    def subscriptions(self, request):
        """Вывод всех подписок пользователя"""
        followers = get_list_or_404(
            CustomUser, following__user=self.request.user
        )
        page = self.paginate_queryset(followers)
        serializer = FollowSerializer(
                page, context={'request': request}, many=True
            )
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=FollowSerializer
    )
    def subscribe(self, request, id):
        """Подписка и отписка на автора"""
        author_id = id
        if request.method == 'POST':
            author = get_object_or_404(CustomUser, id=author_id)
            serializer = FollowSerializer(author, context={'request': request})
            serializer.validate(serializer.data)
            Follow.objects.create(
                user=request.user, author=author
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        user_id = request.user.id
        subscribe = get_object_or_404(
            Follow, user__id=user_id, author__id=author_id
        )
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
