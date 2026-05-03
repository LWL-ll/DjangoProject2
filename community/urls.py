from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # 页面路由
    path('bilei/', views.bilei_page, name='bilei'),
    path('recommend/', views.recommend_page, name='recommend'),
    path('tuijian/', views.tuijian_page, name='tuijian'),

    # API 路由（建议添加 api/ 前缀以区分）
    path('api/posts/', views.get_posts, name='get_posts'),
    path('api/post/create/', views.create_post, name='create_post'),
    path('api/post/<int:post_id>/', views.get_post_detail, name='get_post_detail'),
    path('api/post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('api/post/<int:post_id>/comment/', views.create_comment, name='create_comment'),
]