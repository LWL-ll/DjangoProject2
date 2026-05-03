from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    """帖子模型"""
    
    CATEGORY_CHOICES = [
        ('fast-food', '快餐汉堡'),
        ('chinese-food', '中餐美食'),
        ('light-food', '轻食沙拉'),
        ('dessert', '甜品蛋糕'),
        ('snack', '小吃零食'),
        ('milk-tea', '奶茶饮品'),
    ]
    
    POST_TYPE_CHOICES = [
        ('recommend', '推荐'),
        ('review', '避雷'),
        ('discussion', '讨论'),
    ]
    
    # 推荐等级
    LEVEL_CHOICES = [
        ('highly-recommend', '强烈推荐'),
        ('recommend', '推荐'),
        ('normal', '一般'),
    ]
    
    # 分类
    category = models.CharField('分类', max_length=20, choices=CATEGORY_CHOICES, default='fast-food')
    
    # 基本信息
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    post_type = models.CharField('帖子类型', max_length=20, choices=POST_TYPE_CHOICES, default='recommend')
    
    # 推荐帖子相关字段
    shop_name = models.CharField('店铺名称', max_length=200, blank=True)
    shop_address = models.CharField('店铺位置', max_length=300, blank=True)
    level = models.CharField('推荐等级', max_length=20, choices=LEVEL_CHOICES, blank=True)

    # 作者信息
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者', related_name='posts')

    # 封面图
    cover_image = models.ImageField('封面图', upload_to='posts/covers/', blank=True, null=True)

    # 统计数据
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    comments_count = models.PositiveIntegerField('评论数', default=0)

    # 状态和时间
    is_published = models.BooleanField('是否发布', default=True)
    is_top = models.BooleanField('是否置顶', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ['-is_top', '-created_at']
        verbose_name = '帖子'
        verbose_name_plural = '帖子'

    def __str__(self):
        return self.title

    def increment_views(self):
        """增加浏览量"""
        self.views += 1
        self.save(update_fields=['views'])

    def increment_likes(self):
        """增加点赞数"""
        self.likes += 1
        self.save(update_fields=['likes'])

    def decrement_likes(self):
        """减少点赞数"""
        if self.likes > 0:
            self.likes -= 1
            self.save(update_fields=['likes'])

    def increment_comments(self):
        """增加评论数"""
        self.comments_count += 1
        self.save(update_fields=['comments_count'])

    def decrement_comments(self):
        """减少评论数"""
        if self.comments_count > 0:
            self.comments_count -= 1
            self.save(update_fields=['comments_count'])


class PostImage(models.Model):
    """帖子图片模型 - 用于存储帖子中的多张图片"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='帖子')
    image = models.ImageField('图片', upload_to='posts/images/')
    caption = models.CharField('图片说明', max_length=200, blank=True)
    order = models.PositiveIntegerField('排序', default=0, help_text='数字越小越靠前')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = '帖子图片'
        verbose_name_plural = '帖子图片'

    def __str__(self):
        return f'{self.post.title} - 图片{self.order}'


class Comment(models.Model):
    """评论模型"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='帖子')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                              related_name='replies', verbose_name='父评论',
                              help_text='如果是对评论的回复，选择父评论')

    # 评论者信息
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者', related_name='comments')

    # 评论内容
    content = models.TextField('评论内容')

    # 点赞数
    likes = models.PositiveIntegerField('点赞数', default=0)

    # 时间
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return f'{self.author.username} 评论了 {self.post.title}'

    def increment_likes(self):
        """增加点赞数"""
        self.likes += 1
        self.save(update_fields=['likes'])

    def decrement_likes(self):
        """减少点赞数"""
        if self.likes > 0:
            self.likes -= 1
            self.save(update_fields=['likes'])

    def is_reply(self):
        """判断是否是回复"""
        return self.parent is not None


class PostLike(models.Model):
    """帖子点赞记录模型 - 防止重复点赞"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_records', verbose_name='帖子')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='post_likes')
    liked_at = models.DateTimeField('点赞时间', auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']  # 同一用户只能点赞一次
        ordering = ['-liked_at']
        verbose_name = '帖子点赞记录'
        verbose_name_plural = '帖子点赞记录'

    def __str__(self):
        return f'{self.user.username} 点赞了 {self.post.title}'


class CommentLike(models.Model):
    """评论点赞记录模型"""

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='like_records', verbose_name='评论')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='comment_likes')
    liked_at = models.DateTimeField('点赞时间', auto_now_add=True)

    class Meta:
        unique_together = ['comment', 'user']
        ordering = ['-liked_at']
        verbose_name = '评论点赞记录'
        verbose_name_plural = '评论点赞记录'

    def __str__(self):
        return f'{self.user.username} 点赞了评论'


class PostView(models.Model):
    """帖子浏览记录模型 - 统计浏览数据"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='view_records', verbose_name='帖子')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                            verbose_name='用户', help_text='未登录用户为NULL')
    ip_address = models.GenericIPAddressField('IP地址')
    user_agent = models.TextField('浏览器信息', blank=True)
    viewed_at = models.DateTimeField('浏览时间', auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        verbose_name = '浏览记录'
        verbose_name_plural = '浏览记录'

    def __str__(self):
        user_info = self.user.username if self.user else '匿名用户'
        return f'{user_info} 浏览了 {self.post.title}'
from django.db import models

# Create your models here.
