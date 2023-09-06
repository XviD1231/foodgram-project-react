from rest_framework import serializers
from ingredients.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    measurement_unit = serializers.CharField(max_length=200)

    class Meta:
        model = Ingredient
        fields = '__all__'
