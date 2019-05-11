from django.db import models
import uuid


def gen_uuid() -> str:
    return str(uuid.uuid4())


class ActiveObjectsManager(models.Manager):
    """
    因为系统中的model实例采用的软删除策略, 因此添加一个活动实例的对象管理器来进行非删除对象的查询
    """

    def get_queryset(self):
        return super(ActiveObjectsManager, self).get_queryset().filter(enabled=True)


class BaseModel(models.Model):
    """
    定制一些通用的行为和字段来为所有数据对象服务
    """
    object_id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    priority = models.IntegerField(default=0, verbose_name='对象的优先级')
    enabled = models.BooleanField(default=True, verbose_name='是否启用')

    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, editable=False)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, editable=False)

    objects = models.Manager()  # 全部对象管理器
    active_objects = ActiveObjectsManager()  # 所有激活状态的查询集合管理器

    class Meta:
        abstract = True

    def __eq__(self, other):
        """
        model实例的uuid主键在新建的时候不包含'-
        """
        if not isinstance(other, self.__class__):
            return False
        return self.object_id == other.object_id

    def __str__(self):
        return f"<{self.__class__.__name__}:{self.pk}>"

    def delete(self, using=None, keep_parents=False, real_delete=False):
        """
        这里重载model实例的删除,默认实现软删除逻辑
        """
        if not real_delete:
            self.enabled = False
            self.save()
        else:
            super(BaseModel, self).delete(using=using, keep_parents=keep_parents)
