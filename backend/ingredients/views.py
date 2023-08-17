from rest_framework import viewsets
from user.permissions import IsAuthorOrReadOnly
from ingredients.serializers import IngredientSerializer
from ingredients.models import Ingredient


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthorOrReadOnly,]
