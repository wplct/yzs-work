import warnings

from django.contrib.auth import get_user_model
from django.test import TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.api = None
        warnings.simplefilter('error')

    def create_default_user(self):
        self.username = 'yzs'
        self.password = '123123123'
        self.user = get_user_model().objects.create_user(self.username, 'yzs@yzs.cn', self.password)


class YzsTestCase(BaseTestCase):
    def register_resource(self, resource):
        from yzs_test.urls import urlpatterns
        from django.conf.urls import url
        from tastypie.api import Api
        from django.urls import include

        if self.api is None:
            self.api = Api(api_name='v1')
        self.api.register(resource)
        urlpatterns.append(url(r'^test_api/', include(self.api.urls)), )

    def tearDown(self):
        from yzs_test.urls import urlpatterns
        from django.urls import URLResolver

        for url in urlpatterns:
            assert isinstance(url, URLResolver)
            if str(url.pattern) == r'^test_api/':
                urlpatterns.remove(url)
