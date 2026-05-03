import logging
from django.shortcuts import render
from django.http import JsonResponse
from lauth.decorators import login_required

logger = logging.getLogger(__name__)


def index(request):
    """
    首页视图（不需要登录即可访问）

    Args:
        request: HTTP 请求对象

    Returns:
        HttpResponse: 渲染后的 parallax.html 页面
    """
    return render(request, 'index.html')


