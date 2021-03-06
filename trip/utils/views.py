from functools import wraps

from utils.response import UnauthorizedJsonResponse


def login_required(view_func):
    """登录校验，没有登录返回401"""

    @wraps(view_func)  # wraps不改变使用装饰器原有函数的结构(如name, doc)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return UnauthorizedJsonResponse()
        return view_func(request, *args, **kwargs)

    return _wrapped_view
