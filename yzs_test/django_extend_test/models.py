from django.db import models

# Create your models here.
from yzs.django_extend.base_model import BaseModel


class Note(BaseModel):
    title = models.CharField(max_length=100, null=True, blank=True)
