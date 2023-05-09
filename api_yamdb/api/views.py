from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .filters import TitleFilterSet
from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAdminorModeratorAuthorOnly, IsAdminOrReadOnly,
                          IsAdminOrSuperuserOnly)
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ReviewSerializers, SignupSerializer,
                          TitleSafeMethodsSerializer,
                          TitleUnsafeMethodsSerializer, UserSerializer)
from api_yamdb.settings import CONFIRMATION_CODE
from reviews.models import Category, Genre, Review, Title
from users.models import User


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewsSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSafeMethodsSerializer
        return TitleUnsafeMethodsSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = (IsAdminorModeratorAuthorOnly,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (
        IsAdminorModeratorAuthorOnly,
        IsAuthenticatedOrReadOnly
    )

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'patch', 'delete',)
    permission_classes = (IsAuthenticated, IsAdminOrSuperuserOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False, methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                if serializer.validated_data.get('role'):
                    serializer.validated_data.pop('role')
                serializer.save()
                return Response(serializer.data)


class SignUpViewSet(views.APIView):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if User.objects.filter(
                username=request.data.get('username'),
                email=request.data.get('email')
        ).exists():
            send_mail(
                'Код подтверждения регистрации',
                f'Вам предоставлен личный код подтверждения '
                f'{CONFIRMATION_CODE}',
                'yamdb@example.com',
                [f'{request.data.get("email")}'],
                fail_silently=False,
            )
            User.objects.filter(
                username=request.data.get('username')
            ).update(confirmation_code=CONFIRMATION_CODE)
            return Response(request.data, status=status.HTTP_200_OK)
        send_mail(
            'Код подтверждения регистрации',
            f'Вам предоставлен личный код подтверждения {CONFIRMATION_CODE}',
            'yamdb@example.com',
            [f'{request.data.get("email")}'],
            fail_silently=False,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(confirmation_code=CONFIRMATION_CODE)
        return Response(
            data=serializer.validated_data,
            status=status.HTTP_200_OK
        )


class GetTokenViewSet(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            data={'token': str(serializer.validated_data)},
            status=status.HTTP_200_OK
        )
