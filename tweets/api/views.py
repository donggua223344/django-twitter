from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tweets.api.serializers import (
    TweetSerializer,
    TweetSerializerForCreate,
    TweetSerializerForDetail,
)
from tweets.models import Tweet
from tweets.services import TweetService
from newsfeeds.services import NewsFeedService
from utils.decorators import required_params
from utils.paginations import EndlessPagination


class TweetViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows users to create, list tweets
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializerForCreate
    pagination_class = EndlessPagination

    # 根据当前用户信息获取相应的推文
    @required_params(params=['user_id'])
    def list(self, request):
        tweets = TweetService.get_cached_tweets(user_id=request.query_params['user_id'])

        tweets = self.paginate_queryset(tweets)

        serializer = TweetSerializer(
            tweets,
            context={'request': request},
            many=True,
        )

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = TweetSerializerForDetail(
            self.get_object(),
            context={'request': request},
        )
        return Response(serializer.data)

    # 在当前用户下创建新的推文
    def create(self, request):
        serializer = TweetSerializerForCreate(
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors
            }, status=400)

        # save will call create method in TweetSerializerForCreate
        tweet = serializer.save()

        # update the tweet in each follower's newsfeed
        NewsFeedService.fanout_to_followers(tweet)

        return Response(TweetSerializer(tweet, context={'request': request}).data, status=201)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
