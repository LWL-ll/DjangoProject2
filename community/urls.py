from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # 页面路由
    path('bilei/', views.bilei_page, name='bilei'),
    path('recommend/', views.recommend_page, name='recommend'),

    # API 路由
    path('api/posts/', views.get_posts, name='get_posts'),
    path('api/posts/create/', views.create_post, name='create_post'),
    path('api/posts/<int:post_id>/', views.get_post_detail, name='get_post_detail'),
    path('api/posts/<int:post_id>/like/', views.like_post, name='like_post'),
    path('api/posts/<int:post_id>/comment/', views.create_comment, name='create_comment'),
]