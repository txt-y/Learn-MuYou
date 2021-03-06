from django.db import models


class TicketTypes(models.IntegerChoices):
    ADULT = 11, '成人票'
    CHILD = 12, '儿童票'


class TicketStatus(models.IntegerChoices):
    # 门票状态
    OPEN = 1, '开放购买'
    CLOSED = 0, '暂未开放'


class EnterWay(models.IntegerChoices):
    # 入园方式
    BY_TICKET = 0, '短信换票入园'
    BY_CODE = 1, '验证码入园'
