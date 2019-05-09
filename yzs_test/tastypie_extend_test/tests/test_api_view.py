from django.contrib.auth import get_user_model
from django.test import TestCase
from yzs.tastypie_extend.base_resource import BaseModelResource, api_view

User = get_user_model()


class UserResource(BaseModelResource):
    class Meta:
        authentication = None
        authorization = None
        object_class = User

    @api_view()
    def a(self):
        pass


class ApiViewTestCase(TestCase):
    def test__is_api(self):
        user_resource = UserResource()
        self.assertEqual(1, len(user_resource.prepend_url_list))
        self.assertEqual('user_a', user_resource.prepend_url_list[0].name)
        self.assertEqual('^(?P<resource_name>user)/a/', str(user_resource.prepend_url_list[0].pattern))
