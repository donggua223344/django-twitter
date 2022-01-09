from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from tweets.models import Tweet


# 因为基本所有的测试都需要创建用户或者创建推文，我们就在这里创建两个通用的函数
class TestCase(DjangoTestCase):

    # 创建新用户
    def create_user(self, username, email=None, password=None):
        if password is None:
            password = 'generic password'
        if email is None:
            email = f'{username}@twitter.com'
        return User.objects.create_user(username, email, password)

    # 创建新推文
    def create_tweet(self, user, content=None):
        if content is None:
            content = 'default tweet content'
        return Tweet.objects.create(user=user, content=content)
