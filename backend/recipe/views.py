from django.http import HttpResponse
from django.db.models import Sum
from rest_framework import viewsets
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_403_FORBIDDEN)
from .serializers import RecipeSerializer
from .models import Recipe, ShoppingCart
from recipe.filters import RecipeFilter
from user.permissions import IsAuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

# В основном все прописываю через декораторы.
# Это касается не только вьюсетов Рецептов но и остального.


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['patch'], url_path='{id}',
            permission_classes=[IsAuthorOrReadOnly,])
    def patch_recipes(self, request, pk=None):
        recipes = self.get_object(pk)
        serializer = RecipeSerializer(recipes, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({
            'message_error': 'Предоставленные данные не могут быть обработаны.'
            }, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='{id}',
            permission_classes=[IsAuthorOrReadOnly])
    def delete_recipes(self, request, pk=None):
        author_recipes = Recipe.objects.filter(author=request.user, id=pk)
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
    def favorite_recipe(self, request, pk=None):
        recipe = self.get_object()
        if self.request.method == 'POST':
            if request.user.is_authenticated:
                request.user.favorites.add(recipe)
                return Response({
                    'message': 'Рецепт успешно добавлен в избранное!'
                    }, status=HTTP_201_CREATED)
            else:
                return Response({'error_message': 'Для того чтобы добавлять'
                                'рецепт в избранное вам необходимо'
                                 'зарегестрироваться.'},
                                status=HTTP_401_UNAUTHORIZED)
        elif self.request.method == 'DELETE':
            if request.user.is_authenticated:
                request.user.favorites.remove(recipe)
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
        if self.request.method == 'POST':
            if user == user:
                shopping_cart = ShoppingCart.objects.create(user=user)
                shopping_cart.recipes.add(recipe)
                return Response(
                    {'message': 'Рецепт успешно добавлен в список покупок'},
                    status=HTTP_201_CREATED)
            return Response(
                {'error_message': 'Рецепт не существует'},
                status=HTTP_204_NO_CONTENT)
        elif self.request.method == 'DELETE':
            if user == user:
                shopping_cart = ShoppingCart.objects.get(user=user)
                shopping_cart.recipes.remove(recipe)
                return Response(
                    {'message': 'Рецепт из списка покупок успешно удален.'},
                    status=HTTP_204_NO_CONTENT)
            return Response(
                {'error_message': 'Невозможно удалить рецепт т.к его не'
                 'существует'},
                status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='download_shopping_cart',
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user=user).first()
        if not shopping_cart:
            return Response({'message': 'Ваш список покупок пуст.'},
                            status=HTTP_204_NO_CONTENT)
        recipes = shopping_cart.recipes.all()
        ingredients_summary = (
            recipes.values('ingredients__name',
                           'ingredients__measurement_unit')
            .annotate(total_quantity=Sum('recipe_ingredients__amount'))
        )
        title = 'Список покупок'
        pdfmetrics.registerFont(
            TTFont
            ('Ubuntu',
             'D:/Dev/foodgram-project-react/backend/recipe/fonts/Ubuntu-R.ttf')
             )
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{title}.pdf"'
        pdf = canvas.Canvas(response)
        pdf.setTitle(title)
        text = pdf.beginText(40, 400)
        text.setFont('Ubuntu', 14)
        text.setFillColor(colors.orchid)
        for ingredient in ingredients_summary:
            ingredient_name = ingredient['ingredients__name']
            measurement_unit = ingredient['ingredients__measurement_unit']
            total_quantity = ingredient['total_quantity']
            text.textLine(
                f'{ingredient_name} ({measurement_unit}) — {total_quantity}')

        pdf.drawText(text)
        pdf.save()

        return response
