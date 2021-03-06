from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.models import CommonModel


class User(AbstractUser):
    nickname = models.CharField(verbose_name='昵称', max_length=32, null=True, blank=True)
    avatar = models.ImageField('头像', upload_to='medias/avatar/%Y%m', null=True, blank=True)

    class Meta:
        db_table = 'account_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def add_login_record(self, user, request):
        self.login_record.create(user=user, username=user.username, ip=request.META.get('REMOTE_ADDR', None),
                                 version=request.headers.get('version', None),
                                 source=request.headers.get('source', None))


class Profile(models.Model):
    # 用户详细信息表
    SEX_CHOICES = ((0, '女'), (1, '男'), (2, '保密'))
    username = models.CharField('用户名', max_length=64, editable=False, null=True, blank=True)
    user = models.OneToOneField(to='User', related_name='profile', on_delete=models.CASCADE, verbose_name='关联用户')
    sex = models.SmallIntegerField('性别', choices=SEX_CHOICES, default=2)
    age = models.SmallIntegerField('年龄', null=True, blank=True)
    real_name = models.CharField('真实姓名', max_length=20, null=True, blank=True)
    email = models.CharField('邮箱', max_length=128, null=True, blank=True)
    is_email_valid = models.BooleanField('邮箱验证', default=False)
    phone_no = models.CharField('手机号', max_length=11, null=True, blank=True)
    is_phone_valid = models.BooleanField('手机号验证', default=False)

    source = models.CharField('登录来源', max_length=16, null=True, blank=True)
    version = models.CharField('版本', max_length=16, null=True, blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户详情表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class LoginRecord(models.Model):
    # 用户登录日志
    user = models.ForeignKey(to='User', related_name='login_record', on_delete=models.CASCADE, verbose_name='关联用户')
    username = models.CharField('用户名', max_length=64, null=True, blank=True)
    ip = models.CharField('IP', max_length=32, null=True, blank=True)
    address = models.CharField('地址', max_length=32, null=True, blank=True)
    source = models.CharField('登录来源', max_length=16, null=True, blank=True)
    version = models.CharField('版本', max_length=16, null=True, blank=True)

    created_at = models.DateTimeField('登录时间', auto_now_add=True)

    class Meta:
        db_table = 'login_record'
        verbose_name = '用户日志表'
        verbose_name_plural = verbose_name
