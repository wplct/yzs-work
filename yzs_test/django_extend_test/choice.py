from yzs.django_extend.base_choice import Choice


class NoteColor(Choice):
    RED = (1, 'red')
    GREEN = (2, 'green')
