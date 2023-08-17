from rest_framework import serializers
from recipe.models import Recipe
from ingredients.serializers import IngredientSerializer
from tags.serializers import TagSerializer
from user.serializers import UserSerializer


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.BooleanField(source='favorited_by__user',
                                            read_only=True)
    is_in_shopping_cart = serializers.BooleanField(
        source='is_in_shopping_cart__user', read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')
