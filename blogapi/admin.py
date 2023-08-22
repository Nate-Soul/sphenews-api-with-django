from django.contrib import admin
from django.utils.text import slugify
from .models import Article, Category, Tag, Comment

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {
                            'slug': (slugify('title'),),   
                        }
    
class CategoryAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {
        'slug': (slugify('name'),),
    }
    

class TagAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {
        'slug': (slugify('name'),),
    }
    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)