from django.contrib.auth.models import User
from django.db import models
from tweets.models import Tweet


# Create your models here.
class Comment(models.Model):
    """
    某一条评论只能对应一个推文，但一个推文下面有多个评论
    某一条评论只能对应一个用户，但一个用户可以发布多条评论
    """
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tweet = models.ForeignKey(Tweet, null=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 有在某个 tweet 下排序所有 comments 的需求
        index_together = (('tweet', 'created_at'),)

    def __str__(self):
        return '{} - {} says {} at tweet {}'.format(
            self.created_at,
            self.user,
            self.content,
            self.tweet_id,
        )