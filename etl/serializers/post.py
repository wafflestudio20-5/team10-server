from rest_framework import serializers
from etl.models import *
from .user import UserSimpleSerializer
from .comment import CommentSerializer


# TODO: comment_count 구현
# TODO: Question의 경우 content가 전혀 필요없음. serializer 구분 필요.
class PostSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)
    comment_count = serializers.IntegerField(
        source='comment.count',
        read_only=True,
    )

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {
            **internal_value,
            'created_by': self.context['request'].user,
            'lecture': Class.objects.get(id=self.context['lecture_id']),
            'is_announcement': self.context['is_announcement']
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['content'] = instance.content[:10]
        return rep

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_by', 'created_at', 'comment_count']


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_by', 'created_at', 'comment']
