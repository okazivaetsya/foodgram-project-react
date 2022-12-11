from django_filters import rest_framework as django_filter
from recipes.models import Recipes


class RecipeFilter(django_filter.FilterSet):
    author = django_filter.CharFilter()
    tags = django_filter.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filter.NumberFilter(method='get_favorite')
    is_in_shopping_cart = django_filter.NumberFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipes
        fields = ('tags', 'author')

    def get_favorite(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value == 1:
                return queryset.filter(favorite_recipe__user=user)
        return queryset.exclude(favorite_recipe__user=user)

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value == 1:
                return queryset.filter(shopping_recipe__user=user)
        return queryset.exclude(shopping_recipe__user=user)
