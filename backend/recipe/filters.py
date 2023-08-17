from django_filters import rest_framework as filters
from recipe.models import Recipe


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(field_name='favorited_by__user',
                                         method='filter_by_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart__user',
        method='filter_by_in_shopping_cart'
        )
    author = filters.NumberFilter(field_name='author__id', lookup_expr='exact')
    tags = filters.CharFilter(field_name='tags__slug', method='filter_by_tags')

    class Meta:
        model = Recipe
        fields = []

    def filter_by_favorited(self, queryset, value):
        if value:
            return queryset.filter(favorited_by=self.request.user)
        return queryset

    def filter_by_in_shopping_cart(self, queryset, value):
        if value:
            return queryset.filter(in_shopping_cart=self.request.user)
        return queryset

    def filter_by_tags(self, queryset, value):
        tags_list = value.split(',')
        return queryset.filter(tags__slug__in=tags_list)
