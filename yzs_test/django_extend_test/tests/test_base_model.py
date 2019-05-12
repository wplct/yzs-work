from django.test import TestCase
from django.utils import timezone

from django_extend_test.models import Note
import uuid


class ApiViewTestCase(TestCase):
    def test_base_field_object_id(self):
        """
        测试默认字段 object_id
        :return:
        """

        note = Note()
        note.save()
        self.assertIsInstance(note.pk, uuid.UUID)
        self.assertEqual(note.object_id, note.pk)
        self.assertTrue(note.object_id == note.pk)

        _note = Note.active_objects.filter(pk=note.pk).first()
        self.assertEqual(_note.pk, note.pk)


    def test_base_field_priority(self):
        """
        测试 priority
        :return:
        """
        for i in range(10):
            note = Note()
            note.priority = i
            note.save()

        note_list = Note.active_objects.order_by('priority').all()
        now_priority = -1
        for note in note_list:
            self.assertTrue(note.priority > now_priority)
            now_priority = note.priority

    def test_base_field_enabled(self):
        """
        测试是否启用字段
        :return:
        """

        note = Note()
        note.save()

        # 检查默认值

        self.assertEqual(note.enabled, True)
        note = Note.active_objects.first()
        self.assertEqual(note.enabled, True)

        # 测试删除

        note.delete()
        note = Note.objects.first()
        self.assertEqual(note.enabled, False)
        self.assertEqual(0, Note.active_objects.count())

        # 测试强制删除

        note.delete(real_delete=True)
        self.assertEqual(0, Note.active_objects.count())
        self.assertEqual(0, Note.objects.count())

    def test_base_field_date(self):
        """
        测试创建时间和修改时间
        :return:
        """
        create_at_start = timezone.now()
        note = Note()
        note.save()
        create_at_end = timezone.now()

        self.assertTrue(create_at_start <= note.created_at <= create_at_end)
        self.assertTrue(create_at_start <= note.updated_at <= create_at_end)

        updated_at_start = timezone.now()
        note.title = '1'
        note.save()
        updated_at_end = timezone.now()

        self.assertTrue(updated_at_start <= note.updated_at <= updated_at_end)
