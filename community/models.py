import logging
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.


logger = logging.getLogger(__name__)


class Post(models.Model):
    """
    帖子模型（用于避雷和推荐）
    """
    # 帖子类型选择
    POST_TYPE_CHOICES = [
        ('avoid', '避雷'),
        ('recommend', '推荐'),
    ]

    # 避雷等级选择
    LEVEL_CHOICES = [
        ('super_bad', '超级踩雷'),
        ('bad', '难吃'),
        ('not_recommended', '一般不推荐'),
        ('expensive', '价格太贵'),
        ('hygiene', '卫生差'),
    ]

    # 基础字段
    post_type = models.CharField(
        max_length=20,
        choices=POST_TYPE_CHOICES,
        verbose_name='帖子类型',
        help_text='避雷或推荐'
    )
    shop_name = models.CharField(
        max_length=200,
        verbose_name='店铺名称',
        help_text='店铺或餐厅的名称'
    )
    shop_address = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='店铺位置',
        help_text='店铺所在位置（选填）'
    )
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        verbose_name='避雷等级',
        help_text='仅避雷帖使用'
    )
    content = models.TextField(
        verbose_name='详细内容',
        help_text='避雷原因或推荐理由'
    )
    images = models.JSONField(
        blank=True,
        default=list,
        verbose_name='图片列表',
        help_text='存储图片URL的JSON数组'
    )

    # 统计字段
    views = models.IntegerField(
        default=0,
        verbose_name='浏览量',
        help_text='帖子被查看的次数'
    )
    likes = models.IntegerField(
        default=0,
        verbose_name='点赞数',
        help_text='帖子获得的点赞数'
    )

    # 关联字段
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='作者',
        help_text='发布帖子的用户'
    )

    # 时间字段
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='帖子发布时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='帖子最后修改时间'
    )

    class Meta:
        db_table = 'community_post'
        verbose_name = '帖子'
        verbose_name_plural = '帖子管理'
        ordering = ['-created_at']  # 按创建时间倒序排列

    def __str__(self):
        """返回帖子的字符串表示"""
        type_text = '避雷' if self.post_type == 'avoid' else '推荐'
        return f'{type_text} - {self.shop_name}'

    def increment_views(self):
        """
        增加浏览量

        每次查看帖子时调用此方法，将浏览量加1
        """
        self.views += 1
        self.save(update_fields=['views'])
        logger.info(f'帖子 {self.id} 浏览量+1, 当前: {self.views}')

    def increment_likes(self):
        """
        增加点赞数

        每次点赞时调用此方法，将点赞数加1
        """
        self.likes += 1
        self.save(update_fields=['likes'])
        logger.info(f'帖子 {self.id} 点赞数+1, 当前: {self.likes}')


class Comment(models.Model):
    """
    评论模型
    """
    # 关联帖子
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='关联帖子',
        help_text='该评论所属的帖子'
    )

    # 关联用户
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='评论者',
        help_text='发表评论的用户'
    )

    # 评论内容
    content = models.TextField(
        verbose_name='评论内容',
        help_text='评论的具体内容'
    )

    # 时间字段
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='评论时间',
        help_text='评论发布的时间'
    )

    class Meta:
        db_table = 'community_comment'
        verbose_name = '评论'
        verbose_name_plural = '评论管理'
        ordering = ['created_at']  # 按时间正序排列

    def __str__(self):
        """返回评论的字符串表示"""
        return f'{self.author.username} 评论了 {self.post.shop_name}'


class UserLike(models.Model):
    """
    用户点赞记录模型（防止重复点赞）
    """
    # 关联用户
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        help_text='点赞的用户'
    )

    # 关联帖子
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='帖子',
        help_text='被点赞的帖子'
    )

    # 点赞时间
    liked_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='点赞时间',
        help_text='用户点赞的时间'
    )

    class Meta:
        db_table = 'community_user_like'
        verbose_name = '用户点赞记录'
        verbose_name_plural = '用户点赞记录管理'
        # 确保一个用户对同一个帖子只能点赞一次
        unique_together = ['user', 'post']

    def __str__(self):
        """返回点赞记录的字符串表示"""
        return f'{self.user.username} 点赞了 {self.post.shop_name}'