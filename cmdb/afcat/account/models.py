from django.db import models
from django.contrib.auth.models import User, Group
from afcat.cmdb.models import BaseCustomerInfo

# Create your models here.


class Menus(models.Model):
    """
    用户登录后可以管理的当前系统的菜单
    """
    menu_code = models.CharField(max_length=100)
    menu_name = models.CharField(max_length=200)
    is_avaible = models.IntegerField(default=1)

    def __str__(self):
        return "%s<%s>" % (self.menu_name, self.menu_code)

    class Meta:
        app_label = "account"
        permissions = (
            ("view_menus", "can view menus"),
        )


class Account(models.Model):
    username = models.OneToOneField(User, verbose_name=u'用户名', on_delete=models.CASCADE)
    cust_id = models.CharField(max_length=1024, verbose_name=u"管理客户")
    nickname = models.CharField(max_length=32, verbose_name=u'昵称')
    avatar = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'头像')

    class Meta:
        app_label = "account"
        verbose_name = u'用户'
        verbose_name_plural = u'用户'




