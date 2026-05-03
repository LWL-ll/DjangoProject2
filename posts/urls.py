from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # 帖子列表页
    path('', views.post_list, name='post_list'),
    
    # 6个分类列表页
    path('fast-food/', views.category_list, {'category': 'fast-food'}, name='fast_food'),
    path('chinese-food/', views.category_list, {'category': 'chinese-food'}, name='chinese_food'),
    path('light-food/', views.category_list, {'category': 'light-food'}, name='light_food'),
    path('dessert/', views.category_list, {'category': 'dessert'}, name='dessert'),
    path('snack/', views.category_list, {'category': 'snack'}, name='snack'),
    path('milk-tea/', views.category_list, {'category': 'milk-tea'}, name='milk_tea'),

    # API 接口
    path('api/create/', views.api_create_post, name='api_create_post'),

    # 发布帖子 - 跳转到推荐墙
    path('create/', views.create_post_redirect, name='create_post'),

    # 帖子详情页
    path('<int:post_id>/', views.post_detail, name='post_detail'),

    # 我的帖子
    path('my-posts/', views.my_posts, name='my_posts'),

    # 编辑帖子
    path('<int:post_id>/edit/', views.edit_post, name='edit_post'),

    # 删除帖子
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),

    # 点赞帖子
    path('<int:post_id>/like/', views.like_post, name='like_post'),

    # 添加评论
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),

    # 点赞评论
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),

    # 删除评论
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
