from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from accounts.models import User
from order import choices
from utils.models import CommonModel


class Order(CommonModel):
    """订单"""
    sn = models.CharField('订单编号', max_length=32)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='order_user', verbose_name='关联用户')
    buy_count = models.PositiveIntegerField('购买数量', default=1)
    buy_amount = models.FloatField('总价', default=0.0)

    to_user = models.CharField('收货人', max_length=16)
    to_area = models.CharField('省市区', max_length=32, null=True, blank=True)
    to_address = models.CharField('详细地址', max_length=128, null=True, blank=True)
    to_phone = models.CharField('手机号码', max_length=11)
    remark = models.CharField('备注', max_length=128, null=True, blank=True)

    # 快递信息
    express_type = models.CharField('快递', max_length=32, null=True, blank=True)
    express_no = models.CharField('单号', max_length=32, null=True, blank=True)

    status = models.SmallIntegerField('订单状态', choices=choices.OrderStatus.choices, default=choices.OrderStatus.SUBMIT)
    types = models.SmallIntegerField('订单类型', choices=choices.OrderTypes.choices,
                                     default=choices.OrderTypes.SIGHT_TICKET)

    class Meta:
        db_table = 'order'
        verbose_name = '订单表'
        verbose_name_plural = verbose_name


class OrderItem(CommonModel):
    """ 订单明细 """
    user = models.ForeignKey(to=User, related_name='order_items', on_delete=models.CASCADE, verbose_name='关联用户')
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='order_items', null=True,
                              verbose_name='关联订单')
    # 商品快照
    flash_name = models.CharField('商品名称', max_length=128, null=True, blank=True)
    flash_img = models.ImageField('商品的主图', upload_to='medias/avatar/%Y%m', null=True, blank=True)
    flash_price = models.FloatField('价格', default=0.0)
    flash_origin_price = models.FloatField('原价', default=0.0)
    flash_discount = models.FloatField('折扣', default=0.0)
    count = models.PositiveIntegerField('购买数量', default=1)
    amount = models.FloatField('总额', default=0.0)

    status = models.SmallIntegerField('订单状态', choices=choices.OrderStatus.choices, default=choices.OrderStatus.SUBMIT)
    remark = models.CharField('备注', max_length=255, null=True, blank=True)

    # 复合关联
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'order_item'
        verbose_name = '订单明细表'
        verbose_name_plural = verbose_name


class Payment(CommonModel):
    """ 支付凭证 """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='payments')
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.FloatField('金额', default=0.0, help_text='实际支付的金额')
    sn = models.CharField('流水号', max_length=32, null=True, blank=True)
    third_sn = models.CharField('第三方订单号', max_length=128, null=True, blank=True)

    status = models.SmallIntegerField('支付状态', default=1)

    meta = models.CharField('其他数据', max_length=128, null=True, blank=True)
    remark = models.CharField('备注信息', max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'order_payment'
        verbose_name = '支付信息表'
        verbose_name_plural = verbose_name
