from system.serializers import BaseImageSerializer
from utils.serializers import BaseListPageSerializer, BaseSerializer


class SightListSerializer(BaseListPageSerializer):
    def get_object(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'min_price': obj.min_price,
            'main_img': obj.main_img.url,
            'score': obj.score,
            'province': obj.province,
            'city': obj.city,
            'comment_count': obj.comment_count,
        }


class SightDetailSerializer(BaseSerializer):
    # 景点详情
    def to_dict(self):
        obj = self.obj
        return {
            'id': obj.id,
            'name': obj.name,
            'desc': obj.desc,
            'img': obj.banner_img.url,
            'content': obj.content,
            'score': obj.score,
            'min_price': obj.min_price,
            'province': obj.province,
            'city': obj.city,
            'area': obj.area,
            'town': obj.town,
            'comment_count': obj.comment_count,
            'image_count': obj.image_count,
        }


class SightCommentListSerializer(BaseListPageSerializer):
    # 评论列表
    def get_object(self, obj):
        images = []
        for image in obj.images.filter(is_valid=True):
            images.append(BaseImageSerializer(image).to_dict())
        return {
            'user': {
                'id': obj.user.id,
                'nickname': obj.user.nickname,
            },
            'id': obj.id,
            'content': obj.content,
            'is_top': obj.is_top,
            'love_count': obj.love_count,
            'score': obj.score,
            'images': images,
            'created_at': obj.created_at.strftime('%Y-%m-%d'), }


class SightTicketListSerializer(BaseListPageSerializer):
    # 门票列表
    def get_object(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'desc': obj.desc,
            'types': obj.type,
            'price': obj.sell_price,
            'discount': obj.discount,
            'total_stock': obj.total_stock,
            'remain_stock': obj.remain_stock,
            'return_policy': obj.return_policy,
        }


class SightInfoSerializer(BaseSerializer):
    # 景点详情
    def to_dict(self):
        obj = self.obj
        return {
            'id': obj.sight.id,
            'entry_explain': obj.entry_explain,
            'play_way': obj.play_way,
            'tips': obj.tips,
            'traffic': obj.traffic,
        }


class SightImageListSerializer(BaseListPageSerializer):
    # 门票列表
    def get_object(self, obj):
        a = [1]
        a.append(obj)
        print(a)
        return {
            'id': obj.id,
            'summary': obj.summary,
            'img': obj.img.url
        }


class TicketDetailSerializer(BaseSerializer):
    def to_dict(self):
        obj = self.obj
        return {
            'id': obj.id,
            'name': obj.name,
            'desc': obj.desc,
            'types': obj.type,
            'price': obj.price,
            'sell_price': obj.sell_price,
            'discount': obj.discount,
            'expire_date': obj.expire_date,
            'return_policy': obj.return_policy,
            'has_invoice': obj.has_invoice,
            'entry_way': obj.get_entry_way_display(),
            'tips': obj.tips,
            'remark': obj.remark
        }
