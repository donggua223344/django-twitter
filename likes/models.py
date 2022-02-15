from accounts.services import UserService
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Like(models.Model):
    object_id = models.PositiveIntegerField()  # tweet_id or comment_id
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
    )
    # user liked content_object at created_at
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 这里使用 unique together 也就会建一个 <user, content_type, object_id>的索引
        # unique_together创建的索引具有唯一性，是在数据库层面的限制
        unique_together = (('user', 'content_type', 'object_id'),)
        index_together = (('content_type', 'object_id', 'created_at'),
                          ('user', 'content_type', 'created_at'), )

    def __str__(self):
        return '{} - {} liked {} {}'.format(
            self.created_at,
            self.user,
            self.content_type,
            self.object_id,
        )

    @property
    def cached_user(self):
        return UserService.get_user_through_cache(self.user_id)
