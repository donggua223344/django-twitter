from accounts.api.serializers import UserSerializerForFriendship
from friendships.models import Friendship
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

"""
Django Rest Framework 中的Serializer究竟是做什么的?
(1) 将queryset与model中的实例进行序列化，转换成json格式并返回给api接口
(2) 对数据进行处理
(3) 对数据进行验证
"""


class FollowerSerializer(serializers.ModelSerializer):
    user = UserSerializerForFriendship(source="from_user")

    class Meta:
        model = Friendship
        fields = ('user', 'created_at')


class FollowingSerializer(serializers.ModelSerializer):
    user = UserSerializerForFriendship(source="to_user")

    class Meta:
        model = Friendship
        fields = ('user', 'created_at')


class FriendshipSerializerForCreate(serializers.ModelSerializer):
    from_user_id = serializers.IntegerField()
    to_user_id = serializers.IntegerField()

    class Meta:
        model = Friendship
        fields = ('from_user_id', 'to_user_id')

    # 不能自己follow自己
    def validate(self, attrs):
        if attrs['from_user_id'] == attrs['to_user_id']:
            raise ValidationError({
                'message': 'from_user_id and to_user_id should be different'
            })

        return attrs

    def create(self, validated_data):
        from_user_id = validated_data['from_user_id']
        to_user_id = validated_data['to_user_id']

        return Friendship.objects.create(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
        )
