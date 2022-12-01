from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from recipes.models import Recipe, Ingredients, Tag
from .serializers import (
    RecipeSerializer, IngredientSerializer,
    TagSerializer, UserSerializer)
from rest_framework.pagination import PageNumberPagination
from users.models import FoodgramUser


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AllowAny,)


class IngredientsViewSet(ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class TagsViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class UsersViewSet(ModelViewSet):
    queryset = FoodgramUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
