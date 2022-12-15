import io

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (
    Favorites, Ingredients, IngredientsInRecipes,
    Recipes, ShoppingCart, Tags
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from users.models import CustomUser, Follow

from .filters import IngredientsFilter, RecipeFilter
from .pagination import FoodgramPagination
from .serializers import (
    FollowSerializer, IngredientSerializer,
    RecipePostSerializer, RecipeSerializer,
    SimpleRecipeSerializer, TagsSerializer,
    UserSerializer
)


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

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        """Добавление и удаление рецепта в избранное"""
        recipe_id = pk
        if request.method == 'POST':
            recipe = get_object_or_404(Recipes, id=recipe_id)
            if Favorites.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                raise serializers.ValidationError(
                    {'errors': 'Рецепт уже в избранных.'}
                )
            Favorites.objects.create(user=request.user, recipe=recipe)
            serializer = SimpleRecipeSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user_id = request.user.id
            recipe = get_object_or_404(
                Favorites, user__id=user_id,
                recipe__id=recipe_id
            )
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        """Добавление и удаление рецепта в список покупок"""
        recipe_id = pk
        if request.method == "POST":
            recipe = get_object_or_404(Recipes, id=recipe_id)
            if ShoppingCart.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                raise serializers.ValidationError(
                    {'errors': 'Данный рецепт уже добавлен в список покупок.'}
                )
            serializer = SimpleRecipeSerializer(recipe)
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user_id = request.user.id
            if not ShoppingCart.objects.filter(
                user__id=user_id,
                recipe__id=recipe_id
            ).exists():
                raise serializers.ValidationError(
                    {'errors': 'Такого рецепта нет в списке покупок'}
                )
            recipe = get_object_or_404(
                ShoppingCart, user__id=user_id,
                recipe__id=recipe_id
            )
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def download_shopping_cart(self, request):
        """Формирование и выгрузка pdf со списком покупок"""
        user = request.user
        ingr = IngredientsInRecipes.objects.filter(
            recipe__shopping_cart__user=user
        )
        print('  ')
        print('  ')
        print(f'ингр = {ingr}')
        print('  ')
        print('  ')
        ingredients = IngredientsInRecipes.objects.filter(
            recipe__shopping_cart__user=user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            sum_amount=Sum('amount')
        )
        print('  ')
        print('  ')
        print(f'ингредиенты = {ingredients}')
        print('  ')
        print('  ')
        shoping_list = []
        shoping_list.append('СПИСОК ПОКУПОК:')
        shoping_list.append('---------')
        for ingredient in ingredients:
            shoping_list.append(
                f"{ingredient['ingredient__name']} – "
                f"{ingredient['sum_amount']}"
                f"({ingredient['ingredient__measurement_unit']})"
            )
        pdfmetrics.registerFont(TTFont('Ubuntu', './api/fonts/Ubuntu-C.ttf'))
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        font_size = 15
        p.setFont('Ubuntu', font_size)
        start = 800
        for string_line in shoping_list:
            p.drawString(50, start, string_line)
            start -= 15
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True,
            filename='shopping_list.pdf'
        )


class IngredientsViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с ингредиентами"""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientsFilter


class CreateUserView(UserViewSet):
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
        if page is not None:
            serializer = FollowSerializer(
                page, context={'request': request}, many=True
            )
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, id=None):
        """Подписка и отписка на автора"""
        author_id = id
        if request.method == 'POST':
            author = get_object_or_404(CustomUser, id=author_id)
            if author == request.user:
                raise serializers.ValidationError(
                    {'errors': 'Нельзя подписываться на самого себя.'}
                )
            if self.request.user.follower.filter(author=author).exists():
                raise serializers.ValidationError(
                    {'errors': 'Вы уже подписаны на данного автора.'}
                )
            author = get_object_or_404(CustomUser, id=author_id)
            Follow.objects.create(
                user=request.user, author=author
            )
            serializer = FollowSerializer(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user_id = request.user.id
            subscribe = get_object_or_404(
                Follow, user__id=user_id, author__id=author_id
            )
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
