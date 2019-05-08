import functools


def api_view(url_path: str = None, url_name: str = None, auth: bool = False, allowed_methods: list = None):
    """
    自动包装一个定制的视图的url映射
    url_path: api视图的backend的最后一个路径的名称, 默认为视图方法名称(替换下划线为横线)
    url_name: api视图对应的url定义中的name, 默认为资源类名称+视图方法名称
    auth: 指定是否需要用户验证
    allowed_methods: 用来制定自定义视图允许的请求方法列表
    """

    def view_decorator(view_func):
        view_func._is_api = True
        view_func._url_path = url_path
        view_func._url_name = url_name

        default_allowed_methods = ['get', 'options', 'head']
        final_methods = allowed_methods or default_allowed_methods

        @functools.wraps(view_func)
        def view_wrapper(self, request, *args, **kwargs):
            if auth:
                self.is_authenticated(request)
            self.method_check(request, final_methods)
            return view_func(self, request, *args, **kwargs)

        return view_wrapper

    return view_decorator
