import json
import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment, UserLike

logger = logging.getLogger(__name__)


@login_required
def bilei_page(request):
    """
    显示避雷帖子页面（包含发帖表单和帖子列表）
    
    Args:
        request: HTTP 请求对象
    
    Returns:
        HttpResponse: 渲染后的避雷页面
    """
    from posts.models import Post
    posts = Post.objects.filter(post_type='review').order_by('-created_at')
    
    context = {
        'posts': posts,
        'page_type': 'review'
    }
    return render(request, 'bilei_post.html', context)


@login_required
def recommend_page(request):
    """
    显示推荐帖子页面
    
    Args:
        request: HTTP 请求对象
    
    Returns:
        HttpResponse: 渲染后的推荐页面
    """
    return render(request, 'project_detail.html')


@login_required
def tuijian_page(request):
    """
    显示推荐墙页面（发布推荐帖子）
    
    Args:
        request: HTTP 请求对象
    
    Returns:
        HttpResponse: 渲染后的推荐墙页面
    """
    return render(request, 'tuijian_post.html')


def get_posts(request):
    """
    获取帖子列表接口（支持分页和筛选）
    
    查询参数：
        - post_type: 帖子类型（avoid/recommend）
        - page: 页码
        - level: 避雷等级（可选）
    
    Args:
        request: HTTP 请求对象
    
    Returns:
        JsonResponse: 包含帖子列表的 JSON 响应
    """
    try:
        post_type = request.GET.get('post_type', 'avoid')
        page_number = request.GET.get('page', 1)
        level = request.GET.get('level', None)
        
        logger.info(f'获取帖子列表: 类型={post_type}, 页码={page_number}, 等级={level}')
        
        posts = Post.objects.filter(post_type=post_type)
        
        if level:
            posts = posts.filter(level=level)
        
        paginator = Paginator(posts, 10)
        
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        posts_data = []
        for post in page_obj:
            post_data = {
                'id': post.id,
                'post_type': post.post_type,
                'shop_name': post.shop_name,
                'shop_address': post.shop_address,
                'level': post.get_level_display() if post.post_type == 'avoid' else None,
                'content': post.content,
                'images': post.images if post.images else [],
                'views': post.views,
                'likes': post.likes,
                'author': post.author.username,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'comment_count': post.comments.count()
            }
            posts_data.append(post_data)
        
        return JsonResponse({
            'success': True,
            'data': {
                'posts': posts_data,
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous()
            }
        })
    
    except Exception as e:
        logger.error(f'获取帖子列表失败: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': '获取帖子列表失败，请稍后重试'
        })


@login_required
def create_post(request):
    """
    创建新帖子
    
    请求体（JSON）：
        - post_type: 帖子类型（avoid/recommend）
        - shop_name: 店铺名称
        - shop_address: 店铺位置（可选）
        - level: 避雷等级（避雷帖必填）
        - content: 详细内容
        - images: 图片列表（可选）
    
    Args:
        request: HTTP 请求对象
    
    Returns:
        JsonResponse: 创建结果
    """
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': '请求方法错误'
        }, status=405)
    
    try:
        data = json.loads(request.body)
        
        post_type = data.get('post_type', '').strip()
        shop_name = data.get('shop_name', '').strip()
        shop_address = data.get('shop_address', '').strip()
        level = data.get('level', '').strip()
        content = data.get('content', '').strip()
        images = data.get('images', [])
        
        if post_type not in ['avoid', 'recommend']:
            return JsonResponse({
                'success': False,
                'message': '帖子类型不正确'
            })
        
        if not shop_name:
            return JsonResponse({
                'success': False,
                'message': '请输入店铺名称'
            })
        
        if len(shop_name) > 200:
            return JsonResponse({
                'success': False,
                'message': '店铺名称过长'
            })
        
        if not content:
            return JsonResponse({
                'success': False,
                'message': '请输入详细内容'
            })
        
        if len(content) > 5000:
            return JsonResponse({
                'success': False,
                'message': '内容过长，请控制在5000字以内'
            })
        
        if post_type == 'avoid' and level not in [choice[0] for choice in Post.LEVEL_CHOICES]:
            return JsonResponse({
                'success': False,
                'message': '请选择正确的避雷等级'
            })
        
        post = Post.objects.create(
            post_type=post_type,
            shop_name=shop_name,
            shop_address=shop_address,
            level=level if post_type == 'avoid' else '',
            content=content,
            images=images,
            author=request.user
        )
        
        logger.info(f'用户 {request.user.username} 创建了帖子: {shop_name}')
        
        return JsonResponse({
            'success': True,
            'message': '发布成功',
            'data': {
                'post_id': post.id,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    
    except json.JSONDecodeError:
        logger.warning('创建帖子时收到无效的 JSON 数据')
        return JsonResponse({
            'success': False,
            'message': '无效的请求数据'
        })
    
    except Exception as e:
        logger.error(f'创建帖子失败: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': '发布失败，请稍后重试'
        })


def get_post_detail(request, post_id):
    """
    获取帖子详情
    
    Args:
        request: HTTP 请求对象
        post_id: 帖子ID
    
    Returns:
        JsonResponse: 帖子详情数据
    """
    try:
        post = get_object_or_404(Post, id=post_id)
        
        post.increment_views()
        
        comments = Comment.objects.filter(post=post).select_related('author')
        comments_data = []
        for comment in comments:
            comments_data.append({
                'id': comment.id,
                'content': comment.content,
                'author': comment.author.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        post_data = {
            'id': post.id,
            'post_type': post.post_type,
            'shop_name': post.shop_name,
            'shop_address': post.shop_address,
            'level': post.get_level_display() if post.post_type == 'avoid' else None,
            'content': post.content,
            'images': post.images if post.images else [],
            'views': post.views,
            'likes': post.likes,
            'author': post.author.username,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'comments': comments_data,
            'comment_count': len(comments_data)
        }
        
        if request.user.is_authenticated:
            user_liked = UserLike.objects.filter(
                user=request.user,
                post=post
            ).exists()
            post_data['user_liked'] = user_liked
        else:
            post_data['user_liked'] = False
        
        return JsonResponse({
            'success': True,
            'data': post_data
        })
    
    except Exception as e:
        logger.error(f'获取帖子详情失败: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': '获取帖子详情失败'
        })


@login_required
def like_post(request, post_id):
    """
    点赞帖子
    
    Args:
        request: HTTP 请求对象
        post_id: 帖子ID
    
    Returns:
        JsonResponse: 点赞结果
    """
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': '请求方法错误'
        }, status=405)
    
    try:
        post = get_object_or_404(Post, id=post_id)
        
        if UserLike.objects.filter(user=request.user, post=post).exists():
            return JsonResponse({
                'success': False,
                'message': '您已经点赞过了'
            })
        
        try:
            UserLike.objects.create(user=request.user, post=post)
            post.increment_likes()
            
            logger.info(f'用户 {request.user.username} 点赞了帖子 {post_id}')
            
            return JsonResponse({
                'success': True,
                'message': '点赞成功',
                'data': {
                    'likes': post.likes
                }
            })
        
        except IntegrityError:
            return JsonResponse({
                'success': False,
                'message': '您已经点赞过了'
            })
    
    except Exception as e:
        logger.error(f'点赞帖子失败: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': '点赞失败，请稍后重试'
        })


@login_required
def create_comment(request, post_id):
    """
    发表评论
    
    请求体（JSON）：
        - content: 评论内容
    
    Args:
        request: HTTP 请求对象
        post_id: 帖子ID
    
    Returns:
        JsonResponse: 评论结果
    """
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': '请求方法错误'
        }, status=405)
    
    try:
        post = get_object_or_404(Post, id=post_id)
        
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({
                'success': False,
                'message': '评论内容不能为空'
            })
        
        if len(content) > 1000:
            return JsonResponse({
                'success': False,
                'message': '评论内容过长，请控制在1000字以内'
            })
        
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        
        logger.info(f'用户 {request.user.username} 评论了帖子 {post_id}')
        
        return JsonResponse({
            'success': True,
            'message': '评论成功',
            'data': {
                'comment_id': comment.id,
                'author': request.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': '无效的请求数据'
        })
    
    except Exception as e:
        logger.error(f'发表评论失败: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': '评论失败，请稍后重试'
        })