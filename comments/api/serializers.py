from accounts.api.serializers import UserSerializerForComment
from comments.models import Comment
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tweets.models import Tweet
from likes.services import LikeService


class CommentSerializer(serializers.ModelSerializer):
    # 如果不加这个user = UserSerializer(), 那么下面fields里面的user会以user_id的形式展现
    # Serializer套Serializer不宜套得太深
    user = UserSerializerForComment()
    likes_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    # 从数据库读取并展示的时候，只要可以在model里面可以找到或者访问的属性，在Serializer里面就不需要再创建一遍
    class Meta:
        model = Comment
        fields = (
            'id',
            'tweet_id',
            'user',
            'content',
            'created_at',
            'likes_count',
            'has_liked',
        )

    def get_likes_count(self, obj):
        return obj.like_set.count()

    def get_has_liked(self, obj):
        return LikeService.has_liked(self.context['request'].user, obj)


class CommentSerializerForCreate(serializers.ModelSerializer):
    # 从前端读取并创建的时候，在这两项必须手动添加
    # 因为默认 ModelSerializer 里只会自动包含 user 和 tweet 而不是 user_id 和 tweet_id
    tweet_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ('content', 'tweet_id', 'user_id')

    def validate(self, data):
        tweet_id = data['tweet_id']
        if not Tweet.objects.filter(id=tweet_id).exists():
            raise ValidationError({'message': 'tweet does not exist'})

        return data

    def create(self, validated_data):
        return Comment.objects.create(
            user_id=validated_data['user_id'],
            tweet_id=validated_data['tweet_id'],
            content=validated_data['content'],
        )


class CommentSerializerForUpdate(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # 只有content可以被更改
        fields = ('content',)

    def update(self, instance, validated_data):
        instance.content = validated_data['content']
        instance.save()

        return instance
