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


@login_required
def get_categories(request):
    """
    获取美食分类列表接口（需要登录）

    Args:
        request: HTTP 请求对象

    Returns:
        JsonResponse: JSON 格式的分类数据
    """
    categories = [
        {'id': 1, 'name': '快餐汉堡', 'icon': '🍔'},
        {'id': 2, 'name': '奶茶饮品', 'icon': '🥤'},
        {'id': 3, 'name': '中式正餐', 'icon': '🍜'},
        {'id': 4, 'name': '甜品糕点', 'icon': '🍰'},
        {'id': 5, 'name': '特色小吃', 'icon': '🌮'},
        {'id': 6, 'name': '轻食减脂', 'icon': '🥗'},
    ]

    return JsonResponse({
        'success': True,
        'data': categories
    })


@login_required
def search_foods(request):
    """
    搜索美食接口（需要登录）

    Args:
        request: HTTP 请求对象，GET参数中包含搜索关键字

    Returns:
        JsonResponse: JSON 格式的搜索结果
    """
    keyword = request.GET.get('keyword', '').strip()

    if not keyword:
        return JsonResponse({'success': False, 'message': '请输入搜索关键字'})

    logger.info(f'搜索关键字: {keyword}')

    foods = []

    return JsonResponse({
        'success': True,
        'data': foods,
        'message': f'找到 {len(foods)} 个结果'
    })


def bilei(request):
    """
    避雷帖子页面视图

    Args:
        request: HTTP 请求对象

    Returns:
        HttpResponse: 渲染后的 bilei_post.html 页面
    """
    return render(request, 'bilei_post.html')
