from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import include, re_path
from tastypie.api import Api
from tastypie.authentication import Authentication

from yzs.tastypie_extend.base_resource import BaseModelResource, api_view
from yzs_test.urls import urlpatterns

User = get_user_model()


class ApiViewTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.api = Api(api_name='v1')

    def tearDown(self):
        self.clear_resource()

    def clear_resource(self):
        for _url in urlpatterns:
            if str(_url.pattern) == '^api/':
                urlpatterns.remove(_url)

    def register_resource(self, resource):
        self.api.register(resource)
        urlpatterns.append(re_path(r'^api/', include(self.api.urls)), )

    def test_read_only_field(self):
        """
        测试read_only_field是否有效
        :return:
        """

        class UserResource(BaseModelResource):
            class Meta:
                queryset = User.objects.all()
                resource_name = 'user'
                read_only_field = ['username']

        user_resource = UserResource()
        self.register_resource(user_resource)
        r = self.client.get('/api/v1/user/1/')
        # print(r.json)
