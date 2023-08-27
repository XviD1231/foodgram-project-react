from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from user.serializers import (UserSerializer, SubscriptionSerializer,
                              TokenCustomSerializer, SetPasswordSerializer)
from user.models import User, Subscription
from user.services import SubscribtionService


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['post'], url_path='token/login',
            permission_classes=[AllowAny])
    def login(self, request):
        serializer = TokenCustomSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='set_password',
            permission_classes=[AllowAny])
    def set_password(self, request):
        user = request.user
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        current_password = serializer.validated_data['current_password']
        if current_password and new_password:
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Пароль был успешно обновлен.'},
                                status=HTTP_200_OK)
            else:
                raise PermissionDenied('Старый пароль указан не правильно')
        return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='logout',
            permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'], url_path='subscribe',
            permission_classes=[IsAuthenticated, ])
    def subscribe(self, request, pk=None):
        author = self.get_object()
        user = request.user
        if self.request.method == 'POST':
            if author == user:
                return Response('Вы не можете подписаться на себя',
                                status=HTTP_400_BAD_REQUEST)

            SubscribtionService.subscribe(user, author=author)
            is_subscribed = SubscribtionService.is_user_subscribed(user,
                                                                   author)
            serializer = UserSerializer(author,
                                        context={
                                            'request': request,
                                            'is_subscribed': is_subscribed})
            return Response(status=HTTP_201_CREATED, data=serializer.data)

        if self.request.method == 'DELETE':
            if not SubscribtionService.is_user_subscribed(user, author=author):
                return Response(status=HTTP_400_BAD_REQUEST)
            SubscribtionService.unsubscribe(user, author=author)
            return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='subscriptions',
            permission_classes=[IsAuthenticated, ])
    def subscriptions(self, request):
        subscriptions = Subscription.objects.filter(user=request.user)
        subscribed_users = User.objects.filter(
            id__in=subscriptions.values_list('author_id', flat=True)
        )
        serializer = SubscriptionSerializer(subscribed_users, many=True,
                                            context={'request': request})

        page = self.paginate_queryset(serializer.data)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(status=HTTP_200_OK, data=serializer.data)

    @action(detail=True, methods=['get'], url_path='(?P<id>[^/.]+)/$',
            permission_classes=[AllowAny])
    def profile(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user, context={'request': request})
        return Response(status=HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated], url_path='me')
    def me(self, request):
        user = request.user
        is_subscribed = SubscribtionService.is_user_subscribed(request.user,
                                                               user)
        serializer = UserSerializer(user,
                                    context={'request': request,
                                             'is_subscribed': is_subscribed})
        return Response(serializer.data, status=HTTP_200_OK)
