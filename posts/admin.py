from django.contrib import admin
from .models import Post, PostImage, Comment, PostLike, CommentLike, PostView


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'category', 'post_type', 'author', 
        'views', 'likes', 'comments_count', 'is_published', 'is_top', 'created_at'
    ]
    list_filter = ['category', 'post_type', 'is_published', 'is_top', 'created_at']
    search_fields = ['title', 'content', 'author__username', 'shop_name', 'shop_address']
    readonly_fields = ['views', 'likes', 'comments_count', 'created_at', 'updated_at']
    list_editable = ['is_published', 'is_top']
    list_per_page = 20
    date_hierarchy = 'created_at'


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'caption', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'caption']
    readonly_fields = ['created_at']
    list_per_page = 30


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'parent', 'content_preview', 'likes', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'content', 'post__title']
    readonly_fields = ['likes', 'created_at', 'updated_at']
    list_per_page = 30

    @admin.display(description='评论内容')
    def content_preview(self, obj):
        """显示评论内容预览"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'liked_at']
    list_filter = ['liked_at']
    search_fields = ['user__username', 'post__title']
    readonly_fields = ['liked_at']
    list_per_page = 30


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'comment', 'liked_at']
    list_filter = ['liked_at']
    search_fields = ['user__username', 'comment__content']
    readonly_fields = ['liked_at']
    list_per_page = 30


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['post__title', 'user__username', 'ip_address']
    readonly_fields = ['viewed_at']
    list_per_page = 30
