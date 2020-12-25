from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import include
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
        urlpatterns.append(url(r'^api/', include(self.api.urls)), )

    def test__is_api(self):
        """
        测试is_api是否有效
        :return:
        """

        class UserResource(BaseModelResource):
            class Meta:
                queryset = User.objects.all()
                resource_name = 'user'

            @api_view()
            def a(self, request, *args, **kwargs):
                return self.create_response(request)

        user_resource = UserResource()
        self.register_resource(user_resource)
        r = self.client.get('/api/v1/user/a/')
        self.assertEqual('{"_code": 0, "_message": ""}', r.content.decode())
        self.assertEqual('user_a', user_resource.prepend_url_list[0].name)
        self.assertEqual('^(?P<resource_name>user)/a/', str(user_resource.prepend_url_list[0].pattern))

    def test_url_path_and_url_name(self):
        """
        测试定制url_name 和 url_path
        :return:
        """

        class UserResource(BaseModelResource):
            class Meta:
                object_class = User
                resource_name = 'test_url_path_and_url_name'

            @api_view(url_name='test_url_name', url_path='test_url_path')
            def a(self, request, *args, **kwargs):
                return self.create_response(request)

        user_resource = UserResource()
        self.register_resource(user_resource)
        r = self.client.get('/api/v1/test_url_path_and_url_name/test_url_path/')
        self.assertEqual('{"_code": 0, "_message": ""}', r.content.decode())
        self.assertEqual('test_url_name', user_resource.prepend_url_list[0].name)
        self.assertEqual('^(?P<resource_name>test_url_path_and_url_name)/test_url_path/',
                         str(user_resource.prepend_url_list[0].pattern))

    def _test_method(self, method: str):
        now_resource_name = f'test_method_check_{method}'

        class UserResource(BaseModelResource):
            class Meta:
                object_class = User
                resource_name = now_resource_name

            @api_view(allowed_methods=[method])
            def a(self, request, *args, **kwargs):
                return self.create_response(request)

        user_resource = UserResource()
        self.register_resource(user_resource)
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
        """
        测试allowed_methods是否有效
        :return:
        """
        self._test_method('get')
        self._test_method('post')

    def test_auth(self):
        """
        测试auth选项是否有效
        :return:
        """

        class TestAuthentication(Authentication):
            def is_authenticated(self, request, **kwargs):
                return False

        class UserResource(BaseModelResource):
            class Meta:
                object_class = User
                resource_name = 'test_auth'
                authentication = TestAuthentication()

            @api_view(auth=True)
            def a(self, request, *args, **kwargs):
                return self.create_response(request, {})

        user_resource = UserResource()
        self.register_resource(user_resource)
        r = self.client.get('/api/v1/test_auth/a/')
        self.assertEqual(401, r.status_code)

    def test_single_api(self):
        """
        测试单个对象的api
        :return:
        """
        test_pk = 'e7f7d55a-4c45-4c45-a0b4-6724435168d7'
        test_case = self

        class UserResource(BaseModelResource):
            class Meta:
                object_class = User
                resource_name = 'test_single_api'
                queryset = User.objects.all()

            @api_view(single_api=True)
            def a(self, request, pk, *args, **kwargs):
                test_case.assertEqual(test_pk, pk)
                return self.create_response(request)

        user_resource = UserResource()
        self.register_resource(user_resource)
        r = self.client.get('/api/v1/test_single_api/67ed3642-7b63-4f84-80b0-6cbdafac7253/')

        self.assertEqual(404, r.status_code)
        r = self.client.get(f'/api/v1/test_single_api/{test_pk}/a/')
        self.assertEqual(200, r.status_code)
