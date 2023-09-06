from recipe.base64_decoder import Base64ImageField
from rest_framework import serializers
from ingredients.models import Ingredient
from tags.models import Tag
from recipe.models import Favorited, Recipe, RecipeInIngredient, ShoppingCart
from tags.serializers import TagSerializer
from user.serializers import UserSerializer


class RecipeIngredientSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())

    class Meta:
        fields = ('id', 'amount')

    def to_internal_value(self, data):
        ingredient_id = data['id']
        ingredient = Ingredient.objects.get(id=ingredient_id)
        internal_data = {
            'id': ingredient_id,
            'name': ingredient.name,
            'measurement_unit': ingredient.measurement_unit,
        }
        if 'amount' in data:
            internal_data['amount'] = data['amount']
        return internal_data


class RecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор рецептов. """
    ingredients = RecipeIngredientSerializer(many=True)

    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)

    image = Base64ImageField()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        ingredients_data = validated_data.get('ingredients')
        if ingredients_data is not None:
            RecipeInIngredient.objects.filter(recipe=instance).delete()
            for ingredient_data in ingredients_data:
                ingredient_id = ingredient_data['id']
                amount = ingredient_data.get('amount')
                if amount is None:
                    amount = 0
                RecipeInIngredient.objects.create(recipe=instance,
                                                  ingredient_id=ingredient_id,
                                                  amount=amount)
            tags_data = validated_data.get('tags')
            if tags_data is not None:
                instance.tags.set(tags_data)
            instance.save()
            return instance

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data['id']
            amount = ingredient_data['amount']
            RecipeInIngredient.objects.create(recipe=recipe,
                                              ingredient_id=ingredient_id,
                                              amount=amount)

        recipe.tags.set(tags_data)

        return recipe

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'author',
                  'tags', 'name', 'image', 'text', 'cooking_time')


class RecipeGETSerializer(serializers.ModelSerializer):
    """ Сериализатор рецептов. """
    ingredients = serializers.SerializerMethodField(read_only=True)
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(
        source='is_in_shopping_cart__user', read_only=True)

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=request.user, recipes=obj).exists()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorited.objects.filter(
                user=request.user, recipe=obj).exists()

    def get_ingredients(self, obj):
        ingredients_data = RecipeInIngredient.objects.filter(recipe=obj)
        ingredients = []
        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.get(
                pk=ingredient_data.ingredient.pk)
            ingredients.append({
                'id': ingredient.pk,
                'name': ingredient.name,
                'measurement_unit': ingredient.measurement_unit,
                'amount': ingredient_data.amount
            })
        return ingredients

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')
