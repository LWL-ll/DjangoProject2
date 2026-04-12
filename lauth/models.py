from django.db import models
import random
import string
from datetime import timedelta
from django.utils import timezone

class VerificationCode(models.Model):
    email = models.EmailField('邮箱', max_length=254)
    code = models.CharField('验证码', max_length=6)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    is_used = models.BooleanField('是否已使用', default=False)
    
    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.email} - {self.code}'
    
    @staticmethod
    def generate_code():
        """生成6位数字验证码"""
        return ''.join(random.choices(string.digits, k=6))
    
    @classmethod
    def create_code(cls, email):
        """为指定邮箱创建新的验证码"""
        code = cls.generate_code()
        verification = cls.objects.create(email=email, code=code)
        return verification
    
    def is_valid(self):
        """检查验证码是否有效（5分钟内且未使用）"""
        if self.is_used:
            return False
        expiry_time = self.created_at + timedelta(minutes=5)
        return timezone.now() < expiry_time
