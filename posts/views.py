from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .models import Post, PostImage, Comment, PostLike, CommentLike, PostView


# 分类配置
CATEGORY_NAMES = {
    'fast-food': '快餐汉堡',
    'chinese-food': '中餐美食',
    'light-food': '轻食沙拉',
    'dessert': '甜品蛋糕',
    'snack': '小吃零食',
    'milk-tea': '奶茶饮品',
}


def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def post_list(request):
    """帖子列表页"""
    post_type = request.GET.get('type', 'all')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'latest')

    posts = Post.objects.filter(is_published=True)

    if post_type != 'all':
        posts = posts.filter(post_type=post_type)

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )

    if sort_by == 'hot':
        posts = posts.order_by('-views', '-likes')
    elif sort_by == 'likes':
        posts = posts.order_by('-likes')
    else:
        posts = posts.order_by('-is_top', '-created_at')

    posts = posts.annotate(
        image_count=Count('images'),
        comment_count=Count('comments')
    )

    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category_name': '全部帖子',
        'category': 'all',
        'sort_by': sort_by,
        'post_type': post_type,
        'search_query': search_query,
        'current_path': request.path,
    }
    return render(request, 'category_list.html', context)


@login_required
def category_list(request, category):
    """分类帖子列表页"""
    category_name = CATEGORY_NAMES.get(category, '未知分类')
    sort_by = request.GET.get('sort', 'latest')
    
    posts = Post.objects.filter(
        is_published=True,
        category=category
    )
    
    if sort_by == 'hot':
        posts = posts.order_by('-views', '-likes')
    elif sort_by == 'likes':
        posts = posts.order_by('-likes')
    else:
        posts = posts.order_by('-is_top', '-created_at')
    
    posts = posts.annotate(
        image_count=Count('images'),
        comment_count=Count('comments')
    )
    
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'category_name': category_name,
        'category': category,
        'sort_by': sort_by,
    }
    return render(request, 'category_list.html', context)


@login_required
def post_detail(request, post_id):
    """帖子详情页"""
    post = get_object_or_404(Post, id=post_id, is_published=True)

    # 记录浏览量（同一IP每天只计一次）
    ip_address = get_client_ip(request)
    today = timezone.now().date()

    viewed_today = PostView.objects.filter(
        post=post,
        ip_address=ip_address,
        viewed_at__date=today
    ).exists()

    if not viewed_today:
        post.increment_views()

        user = request.user if request.user.is_authenticated else None
        PostView.objects.create(
            post=post,
            user=user,
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
        )

    # 获取帖子图片
    images = post.images.all()

    # 获取评论（分页）
    comments = post.comments.filter(parent=None).select_related('author').order_by('-created_at')
    comment_paginator = Paginator(comments, 20)
    comment_page = request.GET.get('comment_page')
    comment_page_obj = comment_paginator.get_page(comment_page)

    # 检查当前用户是否已点赞
    user_liked = False
    if request.user.is_authenticated:
        user_liked = PostLike.objects.filter(post=post, user=request.user).exists()

    context = {
        'post': post,
        'images': images,
        'comment_page_obj': comment_page_obj,
        'user_liked': user_liked,
    }
    return render(request, 'post_detail.html', context)


@login_required
def create_post(request):
    """发布帖子页"""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        post_type = request.POST.get('post_type', 'recommend')

        if not title or not content:
            return JsonResponse({'success': False, 'error': '标题和内容不能为空'})

        # 创建帖子
        post = Post.objects.create(
            title=title,
            content=content,
            post_type=post_type,
            author=request.user
        )

        # 处理封面图
        if 'cover_image' in request.FILES:
            post.cover_image = request.FILES['cover_image']
            post.save(update_fields=['cover_image'])

        # 处理多张图片
        images = request.FILES.getlist('images')
        for index, image in enumerate(images):
            PostImage.objects.create(
                post=post,
                image=image,
                order=index
            )

        return JsonResponse({
            'success': True,
            'post_id': post.id,
            'message': '发布成功'
        })

    return render(request, 'posts/create_post.html')


@login_required
def create_post_redirect(request):
    """发布帖子页面 - 跳转到推荐墙"""
    return render(request, 'tuijian_post.html')


@login_required
def my_posts(request):
    """我的帖子"""
    my_posts = Post.objects.filter(author=request.user)

    sort_by = request.GET.get('sort', 'latest')
    if sort_by == 'hot':
        my_posts = my_posts.order_by('-views', '-likes')
    elif sort_by == 'likes':
        my_posts = my_posts.order_by('-likes')
    else:
        my_posts = my_posts.order_by('-created_at')

    my_posts = my_posts.annotate(
        image_count=Count('images'),
        comment_count=Count('comments')
    )

    paginator = Paginator(my_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sort_by': sort_by,
    }
    return render(request, 'posts/my_posts.html', context)


@login_required
def edit_post(request, post_id):
    """编辑帖子"""
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        post_type = request.POST.get('post_type', 'recommend')

        if not title or not content:
            return JsonResponse({'success': False, 'error': '标题和内容不能为空'})

        post.title = title
        post.content = content
        post.post_type = post_type
        post.save()

        return JsonResponse({'success': True, 'message': '更新成功'})

    context = {
        'post': post,
    }
    return render(request, 'posts/edit_post.html', context)


@login_required
def delete_post(request, post_id):
    """删除帖子"""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()

    return JsonResponse({
        'success': True,
        'message': '删除成功'
    })


@login_required
def like_post(request, post_id):
    """点赞帖子"""
    post = get_object_or_404(Post, id=post_id)

    # 检查是否已点赞
    like_record, created = PostLike.objects.get_or_create(
        post=post,
        user=request.user
    )

    if created:
        # 新点赞
        post.increment_likes()
        return JsonResponse({
            'success': True,
            'action': 'liked',
            'likes': post.likes,
        })
    else:
        # 取消点赞
        like_record.delete()
        post.decrement_likes()
        return JsonResponse({
            'success': True,
            'action': 'unliked',
            'likes': post.likes,
        })


@login_required
def add_comment(request, post_id):
    """添加评论"""
    post = get_object_or_404(Post, id=post_id)

    content = request.POST.get('content', '').strip()
    parent_id = request.POST.get('parent_id')

    if not content:
        return JsonResponse({'success': False, 'error': '评论内容不能为空'})

    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id, post=post)

    comment = Comment.objects.create(
        post=post,
        author=request.user,
        content=content,
        parent=parent
    )

    # 更新帖子评论数
    post.increment_comments()

    return JsonResponse({
        'success': True,
        'comment_id': comment.id,
        'author': request.user.username,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
        'is_reply': comment.is_reply(),
    })


@login_required
def like_comment(request, comment_id):
    """点赞评论"""
    comment = get_object_or_404(Comment, id=comment_id)

    like_record, created = CommentLike.objects.get_or_create(
        comment=comment,
        user=request.user
    )

    if created:
        comment.increment_likes()
        return JsonResponse({
            'success': True,
            'action': 'liked',
            'likes': comment.likes,
        })
    else:
        like_record.delete()
        comment.decrement_likes()
        return JsonResponse({
            'success': True,
            'action': 'unliked',
            'likes': comment.likes,
        })


@login_required
def delete_comment(request, comment_id):
    """删除评论"""
    comment = get_object_or_404(Comment, id=comment_id)

    # 只有评论作者或帖子作者可以删除
    if comment.author != request.user and comment.post.author != request.user:
        return JsonResponse({'success': False, 'error': '无权删除此评论'})

    post = comment.post
    comment.delete()

    # 更新帖子评论数
    post.decrement_comments()

    return JsonResponse({'success': True, 'message': '删除成功'})


@login_required
@require_POST
def api_create_post(request):
    """API：发布帖子"""
    try:
        title = request.POST.get('title')
        category = request.POST.get('category')
        content = request.POST.get('content')
        post_type = request.POST.get('post_type', 'recommend')
        shop_addr = request.POST.get('shop_addr', '').strip()
        level_text = request.POST.get('level', '').strip()
        
        if not title or not content:
            return JsonResponse({'success': False, 'error': '请填写完整信息'})
        
        # 避雷帖不需要分类，只发布到避雷页面
        if post_type == 'review':
            category = 'avoid'  # 避雷帖使用特殊分类
        elif not category:
            return JsonResponse({'success': False, 'error': '请选择分类'})
        
        level_map = {
            '强烈推荐': 'highly-recommend',
            '非常好吃': 'recommend',
            '还不错': 'recommend',
            '性价比高': 'normal',
            '环境好': 'normal',
            '超级踩雷': 'avoid',
            '难吃': 'avoid',
            '一般不推荐': 'avoid',
            '价格太贵': 'avoid',
            '卫生差': 'avoid'
        }
        level_value = level_map.get(level_text, '')
        
        post = Post.objects.create(
            title=title,
            content=content,
            category=category,
            post_type=post_type,
            author=request.user,
            shop_name=title,
            shop_address=shop_addr,
            level=level_value
        )
        
        images = request.FILES.getlist('images')
        for image in images:
            PostImage.objects.create(post=post, image=image)
        
        # 根据帖子类型决定重定向页面
        if post_type == 'review':
            # 避雷帖重定向到避雷页面
            redirect_url = '/community/bilei/'
        else:
            # 推荐帖重定向到对应分类页
            category_urls = {
                'fast-food': '/posts/fast-food/',
                'chinese-food': '/posts/chinese-food/',
                'light-food': '/posts/light-food/',
                'dessert': '/posts/dessert/',
                'snack': '/posts/snack/',
                'milk-tea': '/posts/milk-tea/'
            }
            redirect_url = category_urls.get(category, '/posts/')
        
        return JsonResponse({
            'success': True,
            'redirect_url': redirect_url,
            'message': f'发布成功！共上传 {len(images)} 张图片'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
