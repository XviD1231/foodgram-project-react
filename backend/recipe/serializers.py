from rest_framework import serializers
from recipe.models import Recipe, ShoppingCart
from ingredients.serializers import IngredientSerializer
from tags.serializers import TagSerializer
from user.serializers import UserSerializer


class RecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор рецептов. """
    ingredients = IngredientSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.BooleanField(source='favorited_by__user',
                                            read_only=True)
    is_in_shopping_cart = serializers.BooleanField(
        source='is_in_shopping_cart__user', read_only=True)

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ShoppingCart.objects.filter(user=request.user, recipes=obj)
        return False

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')
