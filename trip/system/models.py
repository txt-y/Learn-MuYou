from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models import User
from utils.models import CommonModel


class Slider(CommonModel):
    name = models.CharField('名称', max_length=64)
    desc = models.CharField('描述', max_length=256, null=True, blank=True)
    typrs = models.SmallIntegerField('展现位置', default=10)
    img = models.ImageField('图片地址', max_length=255, upload_to='medias/slider/%Y%m/')
    reorder = models.SmallIntegerField('排序字段', default=0, help_text='数字越大越靠前')
    start_time = models.DateTimeField('生效时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    target_url = models.CharField('目标地址', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'system_slider'
        ordering = ['-reorder']
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ImageRelated(CommonModel):
    img = models.ImageField('图片', upload_to='medias/imagefile/%Y%m/', max_length=256)
    summary = models.CharField('说明', max_length=32, null=True, blank=True)
    user = models.ForeignKey(to=User, verbose_name='上传用户', related_name='images_user', on_delete=models.CASCADE,
                             null=True, blank=True)
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE,verbose_name='关联表')
    object_id = models.IntegerField('关联模型')
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'system_image_related'
        verbose_name = '图片关联'
        verbose_name_plural = verbose_name
