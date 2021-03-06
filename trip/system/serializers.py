from utils.serializers import BaseSerializer


class BaseImageSerializer(BaseSerializer):
    # 序列化图片类
    def to_dict(self):
        image = self.obj
        return {
            'img': image.img.url,
            'summary': image.summary
        }
