from django.urls import path
from .views import (
    ArticleListAPIView, 
    ArticleDetailAPIView, 
    ArticleByAuthorAPIView,
    ArticleByCategoryAPIView,
    ArticleByTagAPIView,
    LikeAPIView, 
    CommentAPIView
)

urlpatterns = [
    path('', ArticleListAPIView.as_view(), name='articles-list'),
    path('<slug:slug>/', ArticleDetailAPIView.as_view(), name='article-detail'),
    path('<slug:slug>/comments/', CommentAPIView.as_view(), name='article-comments'),
    path('<slug:slug>/likes/', LikeAPIView.as_view(), name='article-likes'),
    path('by/<str:username>', ArticleByAuthorAPIView.as_view(), name='articles-by-user'),
    path('in/tag/<slug:tag_slug>', ArticleByTagAPIView.as_view(), name='articles-by-tag'),
    path('in/category/<slug:cat_slug>', ArticleByCategoryAPIView.as_view(), name='articles-by-user'),
]