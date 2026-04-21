from django.db import models
from django.contrib.auth.models import User


class UserPreference(models.Model):
    """
    用户个性化偏好模型
    
    存储用户的饮食偏好信息，用于个性化推荐
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='preferences')
    taste = models.CharField(max_length=20, verbose_name='口味偏好')
    cuisine = models.CharField(max_length=20, verbose_name='菜系偏好')
    budget = models.CharField(max_length=20, verbose_name='预算范围')
    allergy = models.CharField(max_length=200, blank=True, default='', verbose_name='饮食禁忌')
    demand = models.TextField(blank=True, default='', verbose_name='其他需求')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户偏好'
        verbose_name_plural = '用户偏好列表'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.taste}口味 {self.cuisine}"
