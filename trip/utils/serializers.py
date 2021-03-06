class BaseSerializer(object):
    def __init__(self, obj):
        self.obj = obj

    def to_dict(self):
        return {}


class MetaSerializer(object):
    # 分页元数据
    '''
           :param page: 当前第几页
           :param page_count: 总页数
           :param total_count: 总记录数
    '''

    def __init__(self, page, page_count, total_count, *args, **kwargs):
        self.page = page
        self.page_count = page_count
        self.total_count = total_count

    def to_dict(self):
        return {
            'total_count': self.total_count,
            'page_count': self.page_count,
            'current_page': self.page
        }


class BaseListPageSerializer(object):
    # 分页类封装
    def __init__(self, page_obj, paginator=None, object_list=[], *args, **kwargs):
        self.page_obj = page_obj
        self.paginator = paginator if paginator else page_obj.paginator
        self.object_list = object_list if object_list else page_obj.object_list

    def get_object(self, obj):
        return {}

    def to_dict(self):
        page = self.page_obj.number
        page_count = self.paginator.num_pages
        total_count = self.paginator.count
        meta = MetaSerializer(page=page, page_count=page_count, total_count=total_count).to_dict()

        objects = []
        for obj in self.object_list:
            objects.append(self.get_object(obj))
        return {
            'meta': meta,
            'objects': objects
        }
