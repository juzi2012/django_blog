from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.fields import exceptions
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    
    # 评论的顶层，不是回复
    root = models.ForeignKey("self",related_name="root_comment",on_delete=models.DO_NOTHING,null=True)
    # 当前评论的父级
    parent = models.ForeignKey("self",related_name="parent_comment",on_delete=models.DO_NOTHING,null=True)
    # 对谁的回复
    reply_to_user = models.ForeignKey(User,related_name="replies",on_delete=models.DO_NOTHING,null=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-comment_time']
