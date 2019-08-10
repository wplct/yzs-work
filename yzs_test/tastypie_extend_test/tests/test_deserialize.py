import json

from django.contrib.auth import get_user_model

from yzs import BaseTestCase, BaseModelResource, api_view
from yzs.django_extend.base_test_case import YzsTestCase

User = get_user_model()


class DeserializeTest(YzsTestCase):
    def test_deserialize(self):
        post_data = {
            'name': '中文测试数据'
        }
        test_case = self
        class UserResource(BaseModelResource):
            class Meta:
                queryset = User.objects.all()
                resource_name = 'user'

            @api_view(allowed_methods=['post'])
            def a(self, request, *args, **kwargs):
                test_case.assertEqual(post_data,self._deserialize(request))
                return self._create_response(request)

        user_resource = UserResource()
        self.register_resource(user_resource)
        # try:
        self.client.post('/api/v1/user/a/', data=post_data)

