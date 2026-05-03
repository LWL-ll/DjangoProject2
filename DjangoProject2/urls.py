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
    path('auth/', include(('lauth.urls', 'lauth'), namespace='lauth')),
    path('community/', include(('community.urls', 'community'), namespace='community')),
    path('personalize/', include(('personalize.urls', 'personalize'), namespace='personalize')),
    path('posts/', include(('posts.urls', 'posts'), namespace='posts')),
]

# 开发环境下提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
