from django_filters import rest_framework as filters
from recipe.models import Recipe
from rest_framework.filters import BaseFilterBackend
from tags.models import Tag


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(field_name='favorited_by_users',
                                         method='filter_by_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart__user',
        method='filter_by_in_shopping_cart'
    )
    author = filters.NumberFilter(field_name='author__id', lookup_expr='exact')
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                             queryset=Tag.objects.all(),
                                             to_field_name='slug',
                                             conjoined=True)

    def filter_queryset(self, request, queryset, view):
        is_favorited = request.query_params.get('is_favorited')
        if is_favorited and request.user.is_authenticated:
            if is_favorited == '1':
                return queryset.filter(favorited_by__user=request.user)
        return queryset

    def filter_by_favorited(self, queryset, value):
        if value:
            return queryset.filter(favorited_by_users__user=self.request.user)
        return queryset

    def filter_by_in_shopping_cart(self, queryset, value):
        if value:
            return queryset.filter(in_shopping_cart=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'tags')


class FavoritedFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        is_favorited = request.query_params.get('is_favorited')
        if is_favorited and request.user.is_authenticated:
            if is_favorited == '1':
                return queryset.filter(favorited_by_users=request.user)
        return queryset
