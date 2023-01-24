from rest_framework import serializers
from etl.models import *
from .user import UserSimpleSerializer


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {
            **internal_value,
            'created_by': self.context['request'].user,
            'post': Post.objects.get(id=self.context['post_id']),
        }

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_by', 'created_at']


class CommentDetailSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_by', 'created_at']
