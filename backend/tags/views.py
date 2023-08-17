from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.response import Response
from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(id=self.kwargs['id']).first()
        if not obj:
            return Response({'message_error':
                             'Тег с указанным идентификатом отсутсвтует.'},
                            status=HTTP_404_NOT_FOUND)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=HTTP_200_OK)
