from django.urls import path
from . import views

app_name = 'personalize'

urlpatterns = [
    path('', views.gexinghua, name='gexinghua'),
    path('api/save/', views.save_preference, name='save_preference'),
    path('api/get/', views.get_preference, name='get_preference'),
]