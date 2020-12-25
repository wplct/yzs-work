from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
# Create your models here.
from yzs import BaseModel


class Member(BaseModel, AbstractUser):
    show_name = models.CharField(max_length=100, verbose_name='昵称')

    objects = UserManager()

    class Meta:
        verbose_name = verbose_name_plural = '用户'

    def __str__(self):
        return f"<用户:{self.username}>"