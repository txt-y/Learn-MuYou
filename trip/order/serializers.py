from utils.serializers import BaseSerializer, BaseListPageSerializer


class OrderItemSerializer(BaseSerializer):
    # 订单明细
    def to_dict(self):
        obj = self.obj
        return {
            'pk': obj.pk,
            'flash_name': obj.flash_name,
            'flash_img': obj.flash_img.url,
            'flash_price': obj.flash_price,
            'flash_origin_price': obj.flash_origin_price,
            'flash_discount': obj.flash_discount,
            'count': obj.count,
            'amount': obj.amount,
            'remark': obj.remark,
            'object_id': obj.object_id,
            'app_label': obj.content_type.app_label,
            'model': obj.content_type.model,
        }


class OredeDetailSerializer(BaseSerializer):
    # 订单详情
    def to_dict(self):
        obj = self.obj
        items = []
        for item in obj.order_items.all():
            items.append(OrderItemSerializer(item).to_dict())
            return {
                'sn': obj.sn,
                'buy_amount': obj.buy_amount,
                'buy_count': obj.buy_count,
                'types': obj.get_types_display(),
                'status': obj.get_status_display(),
                'created_at': obj.created_at,
                'remark': obj.remark,
                'to_user': obj.to_user,
                'to_area': obj.to_area,
                'to_address': obj.to_address,
                'to_phone': obj.to_phone,
                'express_type': obj.express_type,
                'express_no': obj.express_no,
                'items': items
            }


class OrderListSerializer(BaseListPageSerializer):

    def get_object(self, obj):
        item_first_obj = obj.order_items.first()
        item_first = OrderItemSerializer(item_first_obj).to_dict()
        return {
            'sn': obj.sn,
            'buy_amount': obj.buy_amount,
            'buy_count': obj.buy_count,
            'types': obj.get_types_display(),
            'status': obj.status,
            'created_at': obj.created_at,
            'remark': obj.remark,
            'item_first': item_first
        }


class OredeProfileSerializer(BaseSerializer):
    # 订单详情明细
    def to_dict(self):
        obj = self.obj
        items = []
        for item in obj.order_items.all():
            items.append(OrderItemSerializer(item).to_dict())
            return {
                'sn': obj.sn,
                'buy_amount': obj.buy_amount,
                'buy_count': obj.buy_count,
                'status': obj.get_status_display(),
                'created_at': obj.created_at,
                'items': items
            }
