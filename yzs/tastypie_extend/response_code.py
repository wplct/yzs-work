import warnings


class ResourceCode:
    def __init__(self, default_message: str):
        self.default_message = default_message

    def get_message(self):
        return self.default_message


class ResourceCodeManage:
    def __init__(self):
        self.map = {}

    def register(self, code: int, resource_code: ResourceCode):
        """
        注册错误码对象
        :param code: 错误码
        :param resource_code:
        :return:
        """
        self.map[code] = resource_code

    def get_message(self, code):
        """
        获取错误介绍
        :param code: 错误码
        :return:
        """
        resource_code = self.map.get(code)
        if not resource_code:
            warnings.warn('未知错误码', DeprecationWarning)
            return ""
        return resource_code.get_message()


resource_code_manage = ResourceCodeManage()

