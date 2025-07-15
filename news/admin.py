from django.contrib import admin
from .models import Post, Category, Comment
from modeltranslation.admin import TranslationAdmin

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'dateCreation', 'rating')
    model = Post

class TransPostAdmin(PostAdmin, TranslationAdmin):
    model = Post

class CategoryAdmin(TranslationAdmin):
    model = Category

class CommentAdmin(TranslationAdmin):
    model = Comment


admin.site.register(Post, TransPostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
