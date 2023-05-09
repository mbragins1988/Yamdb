from django.core.validators import RegexValidator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSafeMethodsSerializer(serializers.ModelSerializer):
    """Сериализатор для безопасных методов модели Title"""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, instance):
        all_rating = instance.reviews.aggregate(Avg('score'))
        rating = all_rating.get('score__avg', 0)
        return rating


class TitleUnsafeMethodsSerializer(serializers.ModelSerializer):
    """Сериализатор для небезопасных методов модели Title"""
    genre = serializers.SlugRelatedField(
        read_only=False,
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        read_only=False,
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    """Сериалайзер для комментариев"""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        many=False,
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date",)
        model = Comment


class ReviewSerializers(serializers.ModelSerializer):
    """Сериалайзер для отзывов"""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if not 0 <= value <= 10:
            raise serializers.ValidationError(
                'Укажите целое число в диапазоне от 1 до 10.'
            )
        return value

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data

        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                "По данному отзыву комментарий вами уже написан, "
                "обратите внимание на другие."
            )
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                f"Пользователь '{value}' уже создан"
            )
        return value


class SignupSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=150, required=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]',
                message='Имя пользователя должно быть буквенно-цифровым'
            ),
        ]
    )
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f"Использовать имя '{value}'"
                f" в качестве username запрещено")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                f"Пользователь '{value}' уже создан"
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует')
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=256)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Неверный код подтверждения')
        return RefreshToken.for_user(user).access_token
