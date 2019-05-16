from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.fields import exceptions
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
# Create your models here.

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

# 这里方便其他各个app里面的model继承，然后很方便的拿到read_num
class ReadNumExtend():
    def read_num(self):
        try:
            content_type = ContentType.objects.get_for_model(self)
            read_num = ReadNum.objects.get(content_type=content_type,object_id=self.pk)
            return read_num.read_num
        except exceptions.ObjectDoesNotExist as e:
            return 0

class ReadDetail(models.Model):
    read_num = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')