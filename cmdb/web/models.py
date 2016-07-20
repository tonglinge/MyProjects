from django.db import models

# Create your models here.


class UserProfile(models.Model):
    username = models.CharField('用户名', max_length=200, unique=True)
    email = models.EmailField('邮箱')
    password = models.CharField('密码', max_length=100)

    class Meta:
        verbose_name = '登录用户'
        verbose_name_plural = '用户信息表'

