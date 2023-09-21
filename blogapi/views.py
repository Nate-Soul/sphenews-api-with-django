from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    Comment, 
    Article, 
    Tag, 
    Category,
    Like,
)
from .serializers import (
    CommentSerializer, 
    TagSerializer, 
    CategorySerializer, 
    ArticleSerializer,
    LikeSerializer
)
from core.permissions import (
    IsOWnerAndStaffOrSuperAdmin,
    IsStaffOrSuperAdminOrReadOnly,
    #CanViewDraftArticle, 
    #CanViewPrivateArticle,
)


# Create your views here.
class ArticleListAPIView(APIView):
    permission_classes = [IsStaffOrSuperAdminOrReadOnly,]
    
    def get(self, request, *args, **kwargs):
        articles   = Article.objects.filter(status='published', visibility='public')
        serializer = ArticleSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'slug': slugify(request.data.get('title')),
            'excerpt': request.data.get('excerpt'),
            'content': request.data.get('content'),
            'status': request.data.get('status', 'draft'),
            'visibility': request.data.get('visibility', 'public'),
            'featured_image': request.data.get('featured_image', None),                 
            'is_feature': request.data.get('is_feature', False),
            # 'total_likes': request.data.get('total_likes', 0),
            'author': request.user.id,
        }
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            article = serializer.save()
            
            categories = request.data.get('categories')
            tags = request.data.get('tags')
            if categories:
                article.categories.set(categories)
            if tags:
                article.tags.set(tags)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(APIView):
    permission_classes = [IsOWnerAndStaffOrSuperAdmin,]
    
    def get_object(self, slug):
            return get_object_or_404(Article, slug=slug)
        
    def get(self, request, slug, *args, **kwargs):
        article = self.get_object(slug)
        
        if article.status == 'draft' and (article.author != request.user and not request.user.is_superuser):
            return Response({"detail": "You don't have permission to view this article."}, status=status.HTTP_403_FORBIDDEN)
        
        if article.visibility == 'private' and not request.user.isauthenticated:
            return Response({"detail": "You must be logged in to view this article."}, status=status.HTTP_401_UNAUTHORIZED)        
        
        serializer = ArticleSerializer(article, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, slug, *args, **kwargs):
        article = self.get_object(slug)
        
        data = {
            'title': request.data.get('title', article.title),
            'slug': slugify(request.data.get('title', article.title)),
            'excerpt': request.data.get('excerpt', article.excerpt),
            'content': request.data.get('content', article.content),
            'status': request.data.get('status', article.status),
            'visibility': request.data.get('visibility', article.visibility),
            'featured_image': request.data.get('featured_image', article.featured_image),
            'is_feature': request.data.get('is_feature', article.is_feature),
            'total_likes': request.data.get('total_likes', article.total_likes),
            'author': article.author.id,
        }
        
        serializer = ArticleSerializer(article, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, slug, *args, **kwargs):
        article = self.get_object(slug)
        article.delete()
        return Response({'success': f'{article.title} has been deleted'}, status=status.HTTP_204_NO_CONTENT)



class TagListAPIView(APIView):
    permission_classes = [IsStaffOrSuperAdminOrReadOnly,]
    
    def get(self, request, *args, **kwargs):
        tags   = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'slug': slugify(request.data.get('name')),
        }
        serializer = TagSerializer(data=data)
        if serializer.is_valid():
            serializer.save()                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetailAPIView(APIView):
    permission_classes = [IsStaffOrSuperAdminOrReadOnly,]
    
    def get_object(self, slug):
        return get_object_or_404(Tag, slug=slug)
        
    def get(self, request, slug, *args, **kwargs):
        tag = self.get_object(slug)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, slug, *args, **kwargs):
        tag = self.get_object(slug)
        data = {
            'name': request.data.get('name'),
            'slug': slugify(request.data.get('name')),
        }
        serializer = TagSerializer(tag, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, slug, *args, **kwargs):
        tag = self.get_object(slug)
        tag.delete()
        return Response({'success': f'{tag.name} has been deleted'}, status=status.HTTP_204_NO_CONTENT)


class CategoryListAPIView(APIView):
    permission_classes = [IsStaffOrSuperAdminOrReadOnly,]
    
    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'slug': slugify(request.data.get('name')), 
            'description': request.data.get('description', None),
            'parent': request.data.get('parent', None),
            'is_active': request.data.get('is_active', True),
            'cover_photo': request.data.get('cover_photo', None),
        }
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    permission_classes = [IsStaffOrSuperAdminOrReadOnly,]
    
    def get_object(self, slug):
        return get_object_or_404(Category, slug=slug)
        
    def get(self, request, slug, *args, **kwargs):
        category = self.get_object(slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, slug, *args, **kwargs):
        category = self.get_object(slug)
        data = {
            'name': request.data.get('name', category.name),
            'slug': slugify(request.data.get('name', category.name)), 
            'description': request.data.get('description', category.description),
            'parent': request.data.get('parent', category.parent),
            'is_active': request.data.get('is_active', category.is_active),
            'cover_photo': request.data.get('cover_photo', category.cover_photo),
        }
        serializer = CategorySerializer(category, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, slug, *args, **kwargs):
        category = self.get_object(slug)
        category.delete()
        return Response({'success': f'{category.name} has been deleted'}, status=status.HTTP_204_NO_CONTENT)


class ArticleByAuthorAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated,] 
    
    def get(self, request, username, *args, **kwargs):
        author = get_object_or_404(User, username=username)
        articles = Article.objects.filter(author=author).filter(status="published", visibility="public")
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ArticleByTagAPIView(APIView):
    
    def get(self, request, tag_slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles = Article.objects.filter(tags=tag).filter(status="published", visibility="public")
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ArticleByCategoryAPIView(APIView):
    
    def get(self, request, cat_slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=cat_slug)
        articles = Article.objects.filter(categories=category).filter(status="published", visibility="public")
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

  
class CommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_object(self, slug):
        return get_object_or_404(Article, slug=slug)
    
    def get(self, request, slug, *args, **kwargs):
        article = self.get_object(slug)
        comments = Comment.objects.filter(article = article)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, slug, *args, **kwargs):
        article = self.get_object(slug)
        data = {
            'user': request.user.id,
            'article': article.id,
            'content': request.data.get('content')
        }
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class CommentDetailAPIView(APIView):
    permission_classes = [IsStaffOrSuperAdminOrReadOnly,]
    
    def get_object(self, pk):
        return get_object_or_404(Comment, pk=pk)
        
    def get(self, request, pk, *args, **kwargs):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, *args, **kwargs):
        comment = self.get_object(pk)
        data = {
            'user': comment.user.id,
            'article': comment.article.id,
            'content': request.data.get('content', comment.content)
        }
        serializer = CategorySerializer(comment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        comment = self.get_object(pk)
        comment.delete()
        return Response({'success': f'One comment for article: {comment.article.title} has been deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    
class LikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, slug):
        return get_object_or_404(Article, slug=slug)
    
    
    def get(self, request, slug, *args, **kwargs):
        article = self.get_object(slug)
        likes   = Like.objects.filter(article = article)
        serializer = LikeSerializer(likes, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, slug, *args, **kwargs):
        article = self.get_object(slug)
        
        upvoters = article.likes.all().values_list('user', flat = True)
        if request.user.id in upvoters:
            article.total_likes -= 1
            article.likes.filter(user = request.user).delete()
        else:
            article.total_likes += 1
            upvote = Like(user = request.user, article = article)
            upvote.save()
        article.save()
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)