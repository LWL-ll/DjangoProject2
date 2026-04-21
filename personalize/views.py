from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from .models import UserPreference


def gexinghua(request):
    """
    显示个性化推荐页面
    
    Args:
        request: HTTP 请求对象
    
    Returns:
        HttpResponse: 渲染后的个性化推荐页面
    """
    user_preference = None
    if request.user.is_authenticated:
        user_preference = UserPreference.objects.filter(user=request.user).first()
    
    return render(request, 'gexinghua.html', {'user_preference': user_preference})


@require_POST
@login_required
def save_preference(request):
    """
    保存用户个性化偏好到数据库
    
    Args:
        request: HTTP 请求对象
    
    Returns:
        JsonResponse: 保存结果
    """
    try:
        data = json.loads(request.body)
        
        taste = data.get('taste', '').strip()
        cuisine = data.get('cuisine', '').strip()
        budget = data.get('budget', '').strip()
        allergy = data.get('allergy', '').strip()
        demand = data.get('demand', '').strip()
        
        if not taste or not cuisine or not budget:
            return JsonResponse({
                'success': False,
                'message': '请填写完整的偏好信息'
            })
        
        preference, created = UserPreference.objects.update_or_create(
            user=request.user,
            defaults={
                'taste': taste,
                'cuisine': cuisine,
                'budget': budget,
                'allergy': allergy,
                'demand': demand
            }
        )
        
        return JsonResponse({
            'success': True,
            'message': '保存成功' if created else '更新成功'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'保存失败: {str(e)}'
        })


@require_POST
@login_required
def get_preference(request):
    """
    获取用户的个性化偏好
    
    Args:
        request: HTTP 请求对象
    
    Returns:
        JsonResponse: 用户偏好数据
    """
    try:
        preference = UserPreference.objects.filter(user=request.user).first()
        
        if preference:
            return JsonResponse({
                'success': True,
                'data': {
                    'taste': preference.taste,
                    'cuisine': preference.cuisine,
                    'budget': preference.budget,
                    'allergy': preference.allergy,
                    'demand': preference.demand
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': '未找到偏好数据'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'获取失败: {str(e)}'
        })
