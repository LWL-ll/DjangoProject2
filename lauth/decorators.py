from functools import wraps
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings


def login_required(view_func):
    """
    登录验证装饰器
    
    功能：
    - 如果用户未登录，重定向到登录页面
    - 如果是 AJAX 请求，返回 JSON 错误响应
    - 如果已登录，正常执行视图函数
    
    Args:
        view_func: 需要保护的视图函数
        
    Returns:
        wrapper: 包装后的视图函数
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # 判断是否是 AJAX 请求
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
               request.content_type == 'application/json':
                return JsonResponse({
                    'success': False,
                    'message': '请先登录',
                    'need_login': True,
                    'redirect_url': settings.LOGIN_URL
                }, status=401)
            else:
                # 普通请求，重定向到登录页面
                return redirect(f'{settings.LOGIN_URL}?next={request.path}')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
