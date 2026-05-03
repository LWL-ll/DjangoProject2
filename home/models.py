from django.db import models


class FoodCategory(models.Model):
    """
    美食分类模型

    Attributes:
        name: 分类名称
        icon: 分类图标（emoji或图片路径）
        description: 分类描述
        sort_order: 排序顺序
        is_active: 是否启用
        created_at: 创建时间
        updated_at: 更新时间
    """
    name = models.CharField(max_length=100, verbose_name='分类名称')
    icon = models.CharField(max_length=50, verbose_name='分类图标')
    description = models.TextField(blank=True, default='', verbose_name='分类描述')
    sort_order = models.IntegerField(default=0, verbose_name='排序顺序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'food_category'
        verbose_name = '美食分类'
        verbose_name_plural = '美食分类'
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class Banner(models.Model):
    """
    轮播图模型

    Attributes:
        title: 标题
        image: 图片路径
        link_url: 跳转链接
        description: 描述文字
        sort_order: 排序顺序
        is_active: 是否启用
        created_at: 创建时间
        updated_at: 更新时间
    """
    title = models.CharField(max_length=200, verbose_name='标题')
    image = models.ImageField(upload_to='banners/%Y/%m/', verbose_name='轮播图')
    link_url = models.URLField(blank=True, default='', verbose_name='跳转链接')
    description = models.TextField(blank=True, default='', verbose_name='描述')
    sort_order = models.IntegerField(default=0, verbose_name='排序顺序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'banner'
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'
        ordering = ['sort_order']

    def __str__(self):
        return self.title
