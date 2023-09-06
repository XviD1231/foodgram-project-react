from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from user.permissions import IsAuthorOrReadOnly

from ingredients.filters import IngredientFilter
from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    pagination_class = None

    @action(detail=False, methods=['get'], url_path='ingredients')
    def ingredients_list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='(?P<id>[^/.]+)/$')
    def get_ingredient(self, request, pk=None):
        ingredient = self.get_object(id=pk)
        serializer = self.get_serializer(ingredient)
        return Response(serializer.data, status=HTTP_200_OK)
