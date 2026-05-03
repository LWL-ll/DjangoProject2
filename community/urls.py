from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # 页面路由
    path('bilei/', views.bilei_page, name='bilei'),
    path('recommend/', views.recommend_page, name='recommend'),
    path('tuijian/', views.tuijian_page, name='tuijian'),

    # API 路由

]