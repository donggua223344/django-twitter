from django.db import models
from django.contrib.auth.models import User
from tweets.models import Tweet


# Create your models here.
class NewsFeeds(models.Model):
    # 这里的user是指谁可以看到这条帖子
    # 比如说某个人有3个粉丝，那么这个人发帖后，newsfeed会出现3条新的记录
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('user', 'created_at'),)
        unique_together = (('user', 'tweet'),)
        ordering = ('user', '-created_at')

    def __str__(self):
        return f'{self.created_at} inbox of {self.user}: {self.tweet}'
