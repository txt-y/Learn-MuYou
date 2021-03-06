import re

from django import forms
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.utils.timezone import now
from django.core.cache import cache

from accounts.models import User, Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=11, min_length=11)
    password = forms.CharField(label='密码', widget=forms.PasswordInput, min_length=2, max_length=16)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = ''

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        if not re.search(r'^1[0-9]{10}$', username):
            raise forms.ValidationError('手机号不合法')
        return username

    def clean(self):
        data = super().clean()
        if self.errors:
            return
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('用户名或密码不正确')
        elif not user.is_active:
            raise forms.ValidationError('用户被禁用')
        self.user = user
        return data

    def do_logon(self, request):
        user = self.user
        login(request, user)
        user.last_login = now()
        user.save()
        user.add_login_record(user, request)
        return user


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=11, min_length=11)
    password = forms.CharField(label='密码', widget=forms.PasswordInput, min_length=2, max_length=16)
    nickname = forms.CharField(label='昵称', max_length=10, min_length=1)
    # email = forms.EmailField(label='邮箱', widget=forms.EmailInput, required=True)
    sms_code = forms.CharField(label='验证码', max_length=4, min_length=4)

    def clean_username(self):
        phone_num = self.cleaned_data.get('username', None)
        if not re.search(r'^1[0-9]{10}$', phone_num):
            raise forms.ValidationError('手机号不合法')
        if User.objects.filter(username=phone_num).exists():
            raise forms.ValidationError('手机号已存在')
        return phone_num

    def clean(self):
        data = super().clean()
        if self.errors:
            return
        username = data.get('username', None)
        sms_code = data.get('sms_code', None)
        code = cache.get(f'sms_code_{username}')
        if str(code) != sms_code or sms_code is None:
            raise forms.ValidationError('验证码不正确')
        return data

    @transaction.atomic  # 事务控制
    def do_register(self, request):
        data = self.cleaned_data
        try:
            user = User.objects.create_user(username=data['username'], password=data['password'],
                                            nickname=data['nickname'], last_login=now())
            profile = Profile.objects.create(user=user, username=user.username,
                                             version=request.headers.get('version', None),
                                             source=request.headers.get('source', None))
            login(request, user)
            user.add_login_record(user, request)
            return user, profile
        except Exception as e:
            print(e)
            return None


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        # fields = ('real_name', 'email', 'phone_no', 'sex', 'age')
        fields = '__all__'

    def clean_age(self):  # 自定义表单验证
        age = self.cleaned_data.get('age', None)
        if not 0 <= int(age) <= 120:
            raise forms.ValidationError('年龄只能在0-120之间')
        return age

    def save(self, commit=False):  # 重写保存方法，执行其他业务
        obj = super().save(commit)
        if not obj.source:
            obj.source = 'web'
        obj.save()
        return obj
