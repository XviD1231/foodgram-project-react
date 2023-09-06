from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_403_FORBIDDEN)

from recipe.filters import FavoritedFilterBackend, RecipeFilter
from user.permissions import IsAuthorOrReadOnly
from .models import Favorited, Recipe, ShoppingCart
from .serializers import RecipeGETSerializer, RecipeSerializer

# В основном все прописываю через декораторы.
# Это касается не только вьюсетов Рецептов но и остального.


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly, ]
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination
    filter_backends = [FavoritedFilterBackend, DjangoFilterBackend]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGETSerializer
        else:
            return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['patch'], url_path='(?P<id>[^/.]+)/$',
            permission_classes=[IsAuthorOrReadOnly])
    def patch_recipes(self, request, pk=None):
        recipes = self.get_object(pk)
        serializer = RecipeSerializer(recipes, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({
            'message_error': 'Предоставленные данные не могут быть обработаны.'
        }, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='(?P<id>[^/.]+)/$',
            permission_classes=[IsAuthorOrReadOnly])
    def delete_recipes(self, request, pk=None):
        author_recipes = Recipe.objects.filter(author=request.user, pk=pk)
        recipes = author_recipes.first()
        if author_recipes.exists():
            recipes = author_recipes.first()
            recipes.delete()
            return Response({'message': 'Рецепт успешно удален'},
                            status=HTTP_204_NO_CONTENT)
        else:
            return Response({'error_message': 'Вы не можете удалить'
                             'этот рецепт, т.к вы не являетесь его автором!'},
                            status=HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post', 'delete'], url_path='favorite',
            permission_classes=[IsAuthenticated])
    @method_decorator(login_required, name='dispatch')
    def favorite_recipe(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        if self.request.method == 'POST':
            if request.user.is_authenticated:
                Favorited.objects.get_or_create(user=user, recipe=recipe)
                return Response({
                    'message': 'Рецепт успешно добавлен в избранное!'
                }, status=HTTP_201_CREATED)

        elif self.request.method == 'DELETE':
            if request.user.is_authenticated:
                Favorited.objects.filter(user=user, recipe=recipe).delete()
                return Response({
                    'message': 'Рецепт успешно удален из избранного!'
                }, status=HTTP_204_NO_CONTENT)
            else:
                return Response({
                    'error_message': 'Рецепт не может быть удален из'
                    'избранного т.к он не был добавлен в избранное.'
                }, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'],
            url_path='shopping_cart',
            permission_classes=[IsAuthenticated])
    def add_or_remove_in_shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        user = request.user

        try:
            shopping_cart = ShoppingCart.objects.get(user=user)
        except ShoppingCart.DoesNotExist:
            shopping_cart = ShoppingCart.objects.create(user=user)

        if self.request.method == 'POST':
            shopping_cart.recipes.add(recipe)
            return Response(
                {'message': 'Рецепт успешно добавлен в список покупок'},
                status=HTTP_201_CREATED)
        elif self.request.method == 'DELETE':
            shopping_cart.recipes.remove(recipe)
            return Response(
                {'message': 'Рецепт из списка покупок успешно удален.'},
                status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='download_shopping_cart',
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user=user).first()
        if not shopping_cart:
            return Response({'message': 'Ваш список покупок пуст.'},
                            status=HTTP_204_NO_CONTENT)
        recipes = shopping_cart.recipes.all().prefetch_related(
            'recipe_with_ingredient')
        ingredients_summary = {}
        for recipe in recipes:
            for ingredient in recipe.recipe_with_ingredient.all():
                ingredient_name = ingredient.ingredient.name
                total_quantity = ingredient.amount
                if ingredient_name in ingredients_summary:
                    ingredients_summary[
                        ingredient_name]['total_quantity'] += total_quantity
                else:
                    ingredients_summary[ingredient_name] = {
                        'ingredients__name': ingredient.ingredient.name,
                        'ingredients__measurement_unit':
                        ingredient.ingredient.measurement_unit,
                        'total_quantity': total_quantity
                    }
        ingredient_total = list(ingredients_summary.values())

        title = f'Список покупок - {self.request.user}'
        pdfmetrics.registerFont(
            TTFont('Ubuntu', '/app/recipe/fonts/Ubuntu-R.ttf')
        )
        X = 40
        Y = 400
        FONT_SIZE = 14
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{title}.pdf"'
        pdf = canvas.Canvas(response)
        pdf.setTitle(title)
        text = pdf.beginText(X, Y)
        text.setFont('Ubuntu', FONT_SIZE)
        text.setFillColor(colors.black)
        for ingredient in ingredient_total:
            ingredient_name = ingredient['ingredients__name']
            measurement_unit = ingredient['ingredients__measurement_unit']
            total_quantity = ingredient['total_quantity']
            text.textLine(
                f'{ingredient_name} ({measurement_unit}) — {total_quantity}')

        pdf.drawText(text)
        pdf.save()

        return response
