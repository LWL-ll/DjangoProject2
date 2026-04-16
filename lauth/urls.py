from django.urls import path
from . import views

app_name = 'lauth'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('send-code/', views.send_verification_code, name='send_code'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('register-user/', views.register_user, name='register_user'),
    path('user-login/', views.user_login, name='user_login'),
]