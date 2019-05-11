from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import include
from tastypie.api import Api

from yzs.tastypie_extend.base_resource import BaseModelResource, api_view
from yzs_test.urls import urlpatterns

User = get_user_model()


class ApiViewTestCase(TestCase):
    def setUp(self):
        self.api = Api(api_name='v1')

    def update_resource(self, resource):
        self.api.register(resource)
        for _url in urlpatterns:
            if _url.pattern == '^api/':
                urlpatterns.remove(_url)
                continue
        urlpatterns.append(url(r'^api/', include(self.api.urls)), )

    def test__is_api(self):
        class UserResource(BaseModelResource):
            class Meta:
                queryset = User.objects.all()
                resource_name = 'user'

            @api_view()
            def a(self, *args, **kwargs):
                return self.json_return()

        user_resource = UserResource()
        self.update_resource(user_resource)
        r = self.client.get('/api/v1/user/a/')
        self.assertEqual('{}', r.content.decode())
        self.assertEqual('user_a', user_resource.prepend_url_list[0].name)
        self.assertEqual('^(?P<resource_name>user)/a/', str(user_resource.prepend_url_list[0].pattern))

    def test_url_path_and_url_name(self):
        class UserResource(BaseModelResource):
            class Meta:
                object_class = User
                resource_name = 'user_1'

            @api_view(url_name='test_url_name', url_path='test_url_path')
            def a(self, *args, **kwargs):
                return self.json_return()

        user_resource = UserResource()
        self.update_resource(user_resource)
        r = self.client.get('/api/v1/user_1/test_url_path/')
        self.assertEqual('{}', r.content.decode())
        self.assertEqual('test_url_name', user_resource.prepend_url_list[0].name)
        self.assertEqual('^(?P<resource_name>user_1)/test_url_path/', str(user_resource.prepend_url_list[0].pattern))

    def _test_method(self, method: str):
        now_resource_name = f'test_method_check_{method}'

        class UserResource(BaseModelResource):
            class Meta:
                object_class = User
                resource_name = now_resource_name

            @api_view(allowed_methods=[method])
            def a(self, *args, **kwargs):
                return self.json_return()

        user_resource = UserResource()
        self.update_resource(user_resource)
        r = self.client.get(f'/api/v1/{now_resource_name}/a/')
        if method == 'get':
            self.assertEqual(200, r.status_code)
        else:
            self.assertEqual(405, r.status_code)
        r = self.client.post(f'/api/v1/{now_resource_name}/a/')
        if method == 'post':
            self.assertEqual(200, r.status_code)
        else:
            self.assertEqual(405, r.status_code)

    def test_method_check(self):
        self._test_method('get')
        self._test_method('post')
