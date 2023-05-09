from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenViewSet, ReviewViewSet, SignUpViewSet,
                    TitleViewsSet, UserViewSet)

router = DefaultRouter()

app_name = 'api'

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewsSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('auth/token/', GetTokenViewSet.as_view()),
    path('auth/signup/', SignUpViewSet.as_view()),
    path('', include(router.urls)),
]
