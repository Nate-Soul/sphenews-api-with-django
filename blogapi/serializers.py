from rest_framework import serializers
from .models import (
    Article, 
    Comment, 
    Category, 
    Tag,
    Like
)
from accounts.models import CustomUser as UserModel

class CategorySerializer(serializers.ModelSerializer):
    
    cover_photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'

    def get_cover_photo_url(self, obj):
        if obj.cover_photo:
            return self.context['request'].build_absolute_uri(obj.cover_photo.url)
        return None

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    author      = serializers.SlugRelatedField(slug_field='username', queryset=UserModel.objects.all())
    categories  = CategorySerializer(many=True, read_only=True)
    tags        = TagSerializer(many=True, read_only=True)
    featured_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    def get_featured_image_url(self, obj):
        if obj.featured_image:
            return self.context['request'].build_absolute_uri(obj.featured_image.url)
        return None

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = '__all__'