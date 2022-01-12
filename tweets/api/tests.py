from rest_framework.test import APIClient
from testing.testcases import TestCase
from tweets.models import Tweet

# 注意要加 '/' 结尾，不然会产生 301 redirect
# 这里的全部大写代表常量，说明这些参数不会被更改
TWEET_LIST_API = '/api/tweets/'
TWEET_CREATE_API = '/api/tweets/'


class TweetApiTests(TestCase):

    def setUp(self):
        # anonymous_client 不会登录
        self.anonymous_client = APIClient()

        self.user1 = self.create_user('user1', 'user1@twitter.com')
        self.tweets1 = [
            self.create_tweet(self.user1)
            for _ in range(3)
        ]

        # user1_client 会登陆
        self.user1_client = APIClient()
        self.user1_client.force_authenticate(self.user1)

        self.user2 = self.create_user('user2', 'user2@twitter.com')
        self.tweets2 = [
            self.create_tweet(self.user2)
            for _ in range(2)
        ]

    def test_list_api(self):
        # 请求显示某个用户所有tweets的时候 必须带user_id
        response = self.anonymous_client.get(TWEET_LIST_API)
        self.assertEqual(response.status_code, 400)

        # 正常的请求
        response = self.anonymous_client.get(TWEET_LIST_API,
                                             {'user_id': self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['tweets']), 3)

        response = self.anonymous_client.get(TWEET_LIST_API,
                                             {'user_id': self.user2.id})
        self.assertEqual(len(response.data['tweets']), 2)

        # 测试排序是否是按照规定顺序排序的
        self.assertEqual(response.data['tweets'][0]['id'], self.tweets2[1].id)
        self.assertEqual(response.data['tweets'][1]['id'], self.tweets2[0].id)

    def test_create_api(self):
        # 必须登录
        response = self.anonymous_client.post(TWEET_CREATE_API)
        self.assertEqual(response.status_code, 403)

        # 必须带 content
        response = self.user1_client.post(TWEET_CREATE_API)
        self.assertEqual(response.status_code, 400)
        # content 不能太短
        response = self.user1_client.post(TWEET_CREATE_API, {'content': '1'})
        self.assertEqual(response.status_code, 400)
        # content 不能太长
        response = self.user1_client.post(TWEET_CREATE_API, {
            'content': '0' * 141
        })
        self.assertEqual(response.status_code, 400)

        # 正常发帖
        tweets_count = Tweet.objects.count()
        response = self.user1_client.post(TWEET_CREATE_API, {
            'content': 'Hello World, this is my first tweet!'
        })
        # 2XX 表示成功处理了请求的状态码
        # 200 - 服务器已成功处理了请求
        # 201 - 请求成功并且服务器创建了新的资源
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['id'], self.user1.id)
        self.assertEqual(Tweet.objects.count(), tweets_count + 1)
