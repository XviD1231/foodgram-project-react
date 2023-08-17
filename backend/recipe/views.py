from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_401_UNAUTHORIZED)
from django_filters import rest_framework as filters
from .serializers import RecipeSerializer
from .models import Recipe
from user.permissions import IsAuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination


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


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], url_path='favorite')
    def favorite_recipe(self, request, pk=None):
        recipe = self.get_object()
        if request.user.is_authenticated:
            request.user.favorites.add(recipe)
            return Response(status=HTTP_201_CREATED)
        else:
            return Response({'error_message': 'Для того чтобы добавлять рецепт'
                             'в избранное вам необходимо зарегестрироваться.'},
                            status=HTTP_401_UNAUTHORIZED)
