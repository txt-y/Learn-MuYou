from system.serializers import BaseImageSerializer
from utils.serializers import BaseListPageSerializer, BaseSerializer


class UserSerializer(BaseSerializer):
    # 用户信息
    def to_dict(self):
        user = self.obj
        return {
            'username': user.username,
            'nickname': user.nickname,
            'avatar': user.avatar.url if user.avatar else ''
        }


class UserProfileSerializer(BaseSerializer):
    # 用户详细信息
    def to_dict(self):
        profile = self.obj
        return {
            'real_name': profile.real_name,
            'sex': profile.get_sex_display()  # choices类型返回字符串 get_字段名_display()
        }
