from django_extend_test.choice import NoteColor
from django_extend_test.models import Note
from yzs.django_extend.base_test_case import BaseTestCase


class ChoiceTestCase(BaseTestCase):
    def test_get_display(self):
        note = Note()
        note.save()
        self.assertEqual(note.color, NoteColor.RED)
        self.assertEqual(note.get_color_display(), NoteColor.RED_desc)

