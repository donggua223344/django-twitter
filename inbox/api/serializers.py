from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification

        """
        For example:
        user1 liked tweet2 posted by user2
        actor = user1
        target = tweet2
        verb = like
        """
        fields = (
            'id',
            'actor_content_type',
            'actor_object_id',
            'verb',
            'action_object_content_type',
            'action_object_object_id',
            'target_content_type',
            'target_object_id',
            'timestamp',
            'unread',
        )


class NotificationSerializerForUpdate(serializers.ModelSerializer):
    # Boolean Field会兼容 true, false, "true", "false", "TRUE", "FALSE", 1, 0
    # 这些输入会被转换成 Python 的 Boolean 类型 True/False
    unread = serializers.BooleanField()

    class Meta:
        model = Notification
        fields = ('unread', )

    def update(self, instance, validated_data):
        instance.unread = validated_data['unread']
        instance.save()
        return instance
