import warnings

from django.test import TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.api = None
        warnings.simplefilter('error')

    def register_resource(self, resource):
        from yzs_test.urls import urlpatterns
        from django.conf.urls import url
        from tastypie.api import Api
        from django.urls import include

        if self.api is None:
            self.api = Api(api_name='v1')
        self.api.register(resource)
        urlpatterns.append(url(r'^api/', include(self.api.urls)), )