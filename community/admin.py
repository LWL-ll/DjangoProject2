from django.contrib import admin
from .models import Post, Comment, UserLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_type', 'shop_name', 'shop_address', 'level', 'author', 'views', 'likes', 'created_at']
    list_filter = ['post_type', 'level', 'created_at']
    search_fields = ['shop_name', 'shop_address', 'content']
    readonly_fields = ['views', 'likes', 'created_at', 'updated_at']
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'content', 'post__shop_name']
    readonly_fields = ['created_at']
    list_per_page = 30

    @admin.display(description='评论内容')
    def content_preview(self, obj):
        """显示评论内容预览"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content


@admin.register(UserLike)
class UserLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'liked_at']
    list_filter = ['liked_at']
    search_fields = ['user__username', 'post__shop_name']
    readonly_fields = ['liked_at']
    list_per_page = 30
