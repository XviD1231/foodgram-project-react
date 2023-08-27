from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user.services import SubscribtionService
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор пользователя. """
    username = serializers.RegexField(
        max_length=150,
        regex=r"^[\w.@+-]",
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SubscribtionService.is_user_subscribed(request.user, obj)
        return False

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password', 'is_subscribed')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SubscriptionSerializer(UserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        # Делаю так потому что возникают вечные проблемы с
        # парралельным(цикличным) импортом.
        from recipe.serializers import RecipeSerializer

        recipes = obj.recipes_author.all()
        serializer = RecipeSerializer(recipes, many=True,
                                      context=self.context)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes_author.count()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'recipes_count', 'recipes'
        )


class TokenCustomSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        fields = ('password', 'email')
        extra_kwargs = {'password': {'write_only': True}}


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150, required=True)
    current_password = serializers.CharField(max_length=150, required=True)

    class Meta:
        fields = ('new_password', 'current_password')
        extra_kwargs = {'new_password': {'write_only': True}}
