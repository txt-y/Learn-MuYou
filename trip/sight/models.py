from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# Create your models here.
from accounts.models import User
from system.models import ImageRelated
from utils.models import CommonModel
from sight import choices


class Sight(CommonModel):
    name = models.CharField('名称', max_length=64)
    desc = models.CharField('描述', max_length=256, null=True, blank=True)
    main_img = models.ImageField('主图', max_length=256, upload_to='medias/sight/%Y%m/')
    banner_img = models.ImageField('详情主图', max_length=256, upload_to='medias/sight/%Y%m/')
    # content = models.TextField('详细', null=True, blank=True)
    content = RichTextField('详细', null=True, blank=True)
    score = models.FloatField('评分', default=5)
    province = models.CharField('省份', max_length=32, null=True, blank=True)
    city = models.CharField('城市', max_length=32, null=True, blank=True)
    area = models.CharField('区/县', max_length=32, null=True, blank=True)
    town = models.CharField('乡镇', max_length=32, null=True, blank=True)
    min_price = models.FloatField('最低价格', default=0)
    is_top = models.BooleanField('是否精选', default=False)
    is_hot = models.BooleanField('是否热门', default=False)

    images = GenericRelation(to=ImageRelated, verbose_name='关联图片', related_query_name='rel_sight_images',
                             related_name='rel_sight_ima')

    class Meta:
        db_table = 'sight'
        ordering = ['-updated_at']
        verbose_name = '景点信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def comment_count(self):
        return self.comments_sight.filter(is_valid=True).count()

    @property
    def image_count(self):
        return self.images.filter(is_valid=True).count()


class Info(models.Model):
    # 景点详情
    sight = models.OneToOneField(to=Sight, on_delete=models.CASCADE, verbose_name='关联景点')
    entry_explain = RichTextField('入园参考', null=True, blank=True)
    play_way = RichTextField('特色玩法', null=True, blank=True)
    tips = RichTextField('温馨提示', null=True, blank=True)
    traffic = RichTextField('交通到达', null=True, blank=True)

    class Meta:
        db_table = 'sight_info'
        verbose_name = '景点详情表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sight.name


class Ticket(CommonModel):
    # 门票
    sight = models.ForeignKey(to=Sight, related_name='tickets_sight', on_delete=models.CASCADE, verbose_name='景点门票')
    name = models.CharField('名称', max_length=128)
    desc = models.CharField('描述', max_length=64, null=True, blank=True)
    type = models.SmallIntegerField('类型', help_text='默认成人票', choices=choices.TicketTypes.choices,
                                    default=choices.TicketTypes.ADULT)
    price = models.FloatField('价格(原价)')
    discount = models.FloatField('折扣', default=10)
    total_stock = models.PositiveIntegerField('总库存', default=0)
    remain_stock = models.PositiveIntegerField('剩余库存', default=0)
    expire_date = models.IntegerField('有效期', default=0)
    return_policy = models.CharField('退改政策', max_length=64, default='条件退')
    has_invoice = models.BooleanField('是否提供发票', default=True)
    entry_way = models.SmallIntegerField('入园方式', choices=choices.EnterWay.choices, default=choices.EnterWay.BY_TICKET)
    tips = RichTextField('预定须知', null=True, blank=True)
    remark = RichTextField('其他说明', null=True, blank=True)
    status = models.SmallIntegerField('状态', choices=choices.TicketStatus.choices, default=choices.TicketStatus.OPEN)

    class Meta:
        db_table = 'sirht_ticket'
        verbose_name = '门票表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def sell_price(self):
        return self.price * self.discount / 10


class Comment(CommonModel):
    # 评论和回复
    user = models.ForeignKey(to=User, related_name='comments_user', on_delete=models.CASCADE, verbose_name='评论人')
    sight = models.ForeignKey(to=Sight, related_name='comments_sight', on_delete=models.CASCADE, verbose_name='景点')
    content = models.TextField('评论内容', null=True, blank=True)
    is_top = models.BooleanField('是否置顶', default=False)
    love_count = models.IntegerField('点赞数', default=0)
    score = models.FloatField('评分', default=0)

    ip_address = models.CharField('IP地址', max_length=64, null=True, blank=True)
    is_public = models.SmallIntegerField('是否公开', default=1)
    reply = models.ForeignKey(to='self', related_name='related_name', on_delete=models.CASCADE, verbose_name='回复',
                              blank=True, null=True)

    images = GenericRelation(to=ImageRelated, verbose_name='关联图片', related_query_name='rel_sight_images',
                             related_name='rel_sight_ima')

    class Meta:
        db_table = 'sight_comment'
        ordering = ['-love_count', '-created_at']
        verbose_name = '评论表'
        verbose_name_plural = verbose_name
