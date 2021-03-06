import random
import re

from django import forms
from django.core.cache import cache

from accounts.models import User


class SendSmsCodeForm(forms.Form):
    phone_num = forms.CharField(label='手机号', max_length=11, min_length=11)

    def clean_phone_num(self):
        phone_num = self.cleaned_data.get('phone_num', None)
        if not re.search(r'^1[0-9]{10}$', phone_num):
            raise forms.ValidationError('手机号不合法')
        elif User.objects.filter(username=phone_num).exists():
            raise forms.ValidationError('手机号已注册')
        return phone_num

    def send_sms_code(self):
        # 生成验证码
        try:
            phone_num = self.cleaned_data.get('phone_num', None)
            key = f'sms_code_{phone_num}'  # radis的key
            sms_code = random.randint(1000, 9999)
            time_out = 60 * 5
            # TODO 调用发送短线接口
            cache.set(key, sms_code, timeout=time_out)
            return {
                'phone_num': phone_num,
                'sms_code': sms_code,
                'time_out': time_out
            }
        except Exception as e:
            print(e)
            return None
