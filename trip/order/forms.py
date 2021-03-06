from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import F

from order.models import Order, OrderItem
from sight.models import Ticket
from utils import tools


class SubmitTicketOrderForm(forms.ModelForm):
    ticket_id = forms.IntegerField(label='门票ID')
    play_date = forms.DateField(label='出行时间')

    class Meta:
        model = Order
        fields = ('to_user', 'to_phone', 'buy_count',)

    def __init__(self, *args, **kwargs):  # 重写构造方法，添加字段保存，用作后面计算
        super().__init__(*args, **kwargs)
        self.ticket = None
        self.buy_count=None

    def clean_ticket_id(self):
        ticket_id = self.cleaned_data.get('ticket_id', None)
        ticket = Ticket.objects.select_related('sight').filter(is_valid=True, pk=ticket_id).first()
        self.ticket = ticket
        self.buy_count = self.cleaned_data.get('buy_count', None)
        if ticket is None:
            raise forms.ValidationError('门票信息不存在')
        elif ticket.remain_stock < self.buy_count:
            raise forms.ValidationError('剩余门票不足')
        return ticket_id

    @transaction.atomic  # 事务控制
    def save(self, user, commit=False):
        obj = super().save(commit=commit)
        # 订单表 生成数据并保存
        obj.user = user
        obj.sn = tools.gen_trans_id()  # 生成订单号
        buy_count = self.cleaned_data.get('buy_count', None)  # 获取购买数量
        obj.buy_amount = self.ticket.sell_price * buy_count  # 计算总价格
        obj.save()
        # 门票表 扣减数量
        self.ticket.remain_stock = F('remain_stock') - buy_count
        self.ticket.save()
        # 门票明细表 关联订单明细，保存快照
        ctype = ContentType.objects.get_for_model(Ticket)
        OrderItem.objects.create(
            user=user,
            order=obj,
            flash_name=self.ticket.name,  # 商品名称
            flash_img=self.ticket.sight.main_img,  # 商品主图
            flash_price=self.ticket.sell_price,  # 实付价格(原价*折扣)
            flash_origin_price=self.ticket.price,  # 原价
            flash_discount=self.ticket.discount,  # 折扣
            count=self.buy_count,  # 购买数量
            amount=obj.buy_amount,  # 总额
            content_type=ctype,
            object_id=self.ticket.id,
            remark=f'出行日期：{self.cleaned_data.get("play_date", None)}'  # 备注
        )
        return obj
