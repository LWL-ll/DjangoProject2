"""
URL configuration for DjangoProject2 project.
...
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('auth/', include("lauth.urls")),
    path('community/', include('community.urls')),
    path('personalize/', include('personalize.urls')),
]

# 加上这段代码，让 Django 支持多个 static 目录
urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'community' / 'static')
