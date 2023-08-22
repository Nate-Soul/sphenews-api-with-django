from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    
    name        = models.CharField(max_length=100, unique=True)
    slug        = models.CharField(max_length=100, unique=True)
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    
    name        = models.CharField(max_length=100, unique=True)
    slug        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent      = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    is_active   = models.BooleanField(default=True)
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    
    def __str__(self) -> str:
        return self.name

class Article(models.Model):
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
     
    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )
    
    title = models.CharField(
        unique=True,
        max_length=200,
        verbose_name=_("Article title")
    )
    slug = models.SlugField(
        verbose_name=_("Article safe URL"),
        max_length=100,
        unique=True
    )
    excerpt         = models.TextField(verbose_name=_("Article excerpt"), max_length=300)
    content         = models.TextField(verbose_name=_("Article body"))
    author          = models.ForeignKey(User, on_delete=models.PROTECT)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    visibility      = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    featured_image  = models.ImageField(default="images/default.png", upload_to="images/articles/")
    categories      = models.ManyToManyField(Category)
    tags            = models.ManyToManyField(Tag)
    created         = models.DateTimeField(auto_now_add=True)
    modified        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    
    user    = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.article.title}'
    

class Like(models.Model):
    user    = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='likes', on_delete=models.CASCADE)