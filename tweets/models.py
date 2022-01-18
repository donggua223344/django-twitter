from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from likes.models import Like
from utils.time_helpers import utc_now

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text='who posted this tweet', )
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    # 建立 user 和 created_at 的联合索引 (composite index), 相当于在数据库里新建了一个索引表单
    # 建立了索引后也需要做migration
    class Meta:
        index_together = (('user', 'created_at'), )
        ordering = ('user', '-created_at')

    @property
    def hours_to_now(self):
        # datetime.now不带时区信息，django的DateTimeField是带时区信息的，两者不能直接相减
        return (utc_now() - self.created_at).seconds // 3600

    @property
    def like_set(self):
        return Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Tweet),
            object_id = self.id,
        ).order_by('-created_at')

    def __str__(self):
        # 这里我们更改了默认的print(tweet instance)的时候会显示的内容
        return f'{self.created_at} {self.user}: {self.content}'
