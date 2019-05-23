from django.db import models

# Create your models here.
from django_extend_test.choice import NoteColor
from yzs.django_extend.base_model import BaseModel


class Note(BaseModel):
    title = models.CharField(max_length=100, null=True, blank=True)
    color = models.IntegerField(choices=NoteColor.choices(), default=NoteColor.RED)
