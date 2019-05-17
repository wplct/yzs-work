from django.contrib.auth import get_user_model

from yzs.django_extend.base_test_case import BaseTestCase
from yzs.tastypie_extend.base_resource import BaseModelResource, api_view
from yzs.tastypie_extend.response_code import resource_code_manage, ResourceCode

User = get_user_model()


class ReturnDataTestCase(BaseTestCase):
    def test_resource_code(self):
        resource_code_manage.register(10001, ResourceCode('test'))

        class UserResource(BaseModelResource):
            class Meta:
                queryset = User.objects.all()
                resource_name = 'user'

            @api_view()
            def a(self, request, *args, **kwargs):
                return self.create_response(request, code=1001)

            @api_view()
            def b(self, request, *args, **kwargs):
                return self.create_response(request, code=10001)

        user_resource = UserResource()
        self.register_resource(user_resource)
        # try:
        with self.assertWarns(DeprecationWarning):
            self.client.get('/api/v1/user/a/')

        data = self.client.get('/api/v1/user/b/').json()
        self.assertEqual(data['_code'], 10001)
        self.assertEqual(data['_message'], 'test')
