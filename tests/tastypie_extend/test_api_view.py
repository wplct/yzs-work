from unittest import TestCase

from yzs.tastypie_extend.api_view import api_view


class ApiViewTestCase(TestCase):
    def test__is_api(self):
        class A():
            @api_view()
            def b(self):
                pass

        a = A()
        self.assertTrue(hasattr(a.b, '_is_api'))
