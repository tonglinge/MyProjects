from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class LoginUser(models.Model):
    sex_choices = (
        ('F', u'男'),
        ('M', u'女'),
    )
    head_img_choice = (
        ('head-1.png', '男士1'),
        ('head-3.png', '男士2'),
        ('head-4.png', '男士3'),
        ('head-2.png', '女士1'),
        ('head-5.png', '女士2'),
        ('head-6.png', '女士3')
    )
    user = models.OneToOneField(User)
    fullname = models.CharField(u'昵称', max_length=50)
    sex = models.CharField(u'性别', max_length=2, choices=sex_choices)
    age = models.IntegerField(u'年龄')
    friends = models.ManyToManyField('self', related_name='myfriend',null=True, blank=True)
    head_img = models.CharField(u'头像', choices=head_img_choice, max_length=30, default='head-1.png')
    remark = models.CharField(u'签名', max_length=200, null=True, blank=True)

    def __str__(self):
        return self.fullname


class UserGroup(models.Model):
    owner = models.ForeignKey(LoginUser, related_name='mygroup')
    groupname = models.CharField(u'用户分组名', max_length=100)
    members = models.ManyToManyField("LoginUser", related_name='usergroup_member')
    isdefault = models.IntegerField(default=0)

    def __str__(self):
        return "%s Group: %s" % (self.owner, self.groupname)


class WebGroups(models.Model):
    name = models.CharField(u'群组名', max_length=100)
    owner = models.ForeignKey(LoginUser)
    admins = models.ManyToManyField(LoginUser, related_name='webgroup_admins', null=True, blank=True)
    members = models.ManyToManyField(LoginUser, related_name='webgroup_member', null=True, blank=True)
    brief = models.CharField(u'群组备注', max_length=200, null=True, blank=True)
    max_members = models.IntegerField()

    def __str__(self):
        return self.name