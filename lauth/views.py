from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import VerificationCode
from django.contrib.auth.models import User
import json

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def send_verification_code(request):
    """发送验证码到邮箱"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '请求方法错误'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        
        if not email:
            return JsonResponse({'success': False, 'message': '请输入邮箱地址'})
        
        # 验证邮箱格式
        import re
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, email):
            return JsonResponse({'success': False, 'message': '邮箱格式不正确'})
        
        # 检查邮箱是否已注册
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': '该邮箱已被注册'})
        
        # 生成并保存验证码
        verification = VerificationCode.create_code(email)
        
        # 发送邮件
        subject = '注册验证码'
        message = f'您的验证码是：{verification.code}\n\n验证码有效期为5分钟，请勿泄露给他人。'
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return JsonResponse({'success': True, 'message': '验证码已发送到您的邮箱'})
        except Exception as e:
            # 发送失败时删除验证码记录
            verification.delete()
            return JsonResponse({'success': False, 'message': f'邮件发送失败：{str(e)}'})
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': '无效的请求数据'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'服务器错误：{str(e)}'})

def verify_code(request):
    """验证验证码是否正确"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '请求方法错误'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        code = data.get('code', '').strip()
        
        if not email or not code:
            return JsonResponse({'success': False, 'message': '请提供邮箱和验证码'})
        
        # 查找最新的未使用验证码
        verification = VerificationCode.objects.filter(
            email=email,
            is_used=False
        ).order_by('-created_at').first()
        
        if not verification:
            return JsonResponse({'success': False, 'message': '验证码不存在或已使用'})
        
        if not verification.is_valid():
            return JsonResponse({'success': False, 'message': '验证码已过期'})
        
        if verification.code != code:
            return JsonResponse({'success': False, 'message': '验证码错误'})
        
        # 标记为已使用
        verification.is_used = True
        verification.save()
        
        return JsonResponse({'success': True, 'message': '验证成功'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'服务器错误：{str(e)}'})

def register_user(request):
    """处理用户注册"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '请求方法错误'}, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        verification_code = data.get('verification_code', '').strip()
        
        # 基本验证
        if not username or len(username) < 3:
            return JsonResponse({'success': False, 'message': '用户名至少需要3个字符'})
        
        if not email:
            return JsonResponse({'success': False, 'message': '请输入邮箱地址'})
        
        if not password or len(password) < 6:
            return JsonResponse({'success': False, 'message': '密码至少需要6个字符'})
        
        if not verification_code:
            return JsonResponse({'success': False, 'message': '请输入验证码'})
        
        # 验证验证码
        verification = VerificationCode.objects.filter(
            email=email,
            is_used=False
        ).order_by('-created_at').first()
        
        if not verification or not verification.is_valid() or verification.code != verification_code:
            return JsonResponse({'success': False, 'message': '验证码无效或已过期'})
        
        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': '用户名已被使用'})
        
        # 检查邮箱是否已注册
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': '该邮箱已被注册'})
        
        # 创建用户
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # 标记验证码为已使用
        verification.is_used = True
        verification.save()
        
        return JsonResponse({'success': True, 'message': '注册成功！请登录'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'注册失败：{str(e)}'})
