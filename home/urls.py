from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/categories/', views.get_categories, name='get_categories'),
    path('api/search/', views.search_foods, name='search_foods'),
]
