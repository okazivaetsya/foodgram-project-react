import django_filters as filters

from recipes.models import Ingredients, Recipes, Tags


class RecipeFilter(filters.FilterSet):
    """Фильтры для рецептов. """
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tags.objects.all(),
        to_field_name='slug'
    )
    author = filters.NumberFilter(field_name='author__id')
    is_in_shopping_cart = filters.CharFilter(method='get_is_in_shopping_cart')
    is_favorited = filters.CharFilter(method='get_is_favorited')

    class Meta:
        model = Recipes
        fields = ('tags', 'author',)

    def get_is_in_shopping_cart(self, queryset, name, value):
        return queryset.filter(shopping_cart__user=self.request.user)

    def get_is_favorited(self, queryset, name, value):
        return queryset.filter(Favorites__user=self.request.user)


class IngredientsFilter(filters.rest_framework.FilterSet):
    """Фильтр для ингредиентов"""
    name = filters.rest_framework.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredients
        fields = ('name',)
