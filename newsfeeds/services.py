from newsfeeds.models import NewsFeed
from friendships.services import FriendshipService


# 一般service里面的都是class method, 不需要new instance就可以直接调用
class NewsFeedService(object):

    @classmethod
    def fanout_to_followers(cls, tweet):
        # 错误的方法
        # 不可以将数据库操作放在 for 循环里面，效率会非常低
        # for follower in FriendshipService.get_followers(tweet.user):
        #     NewsFeed.objects.create(
        #         user=follower,
        #         tweet=tweet,
        #     )
        newsfeeds = [
            NewsFeed(user=follower, tweet=tweet)
            for follower in FriendshipService.get_followers(tweet.user)
        ]
        # 自己也能看到自己的推文
        newsfeeds.append(NewsFeed(user=tweet.user, tweet=tweet))
        # bulk_create: 批量创建
        NewsFeed.objects.bulk_create(newsfeeds)
