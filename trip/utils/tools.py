import random

from django.utils.timezone import now


def gen_trans_id(date=None):
    """生成订单号"""
    if date is None:
        date = now()
    str_date = date.strftime('%Y%m%d%H%M%S%f')
    str_random = random.randint(1000, 9999)
    return f'{str_date}{str_random}'
