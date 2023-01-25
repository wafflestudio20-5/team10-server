from rest_framework import serializers
from etl.models import *
from .user import UserSimpleSerializer


class QuestionSerializer(serializers.ModelSerializer):
    content = serializers.CharField(write_only=True)
    created_by = UserSimpleSerializer(read_only=True)
    comment_count = serializers.IntegerField(
        source='comment.count',
        read_only=True,
    )
    hits = serializers.IntegerField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {
            **internal_value,
            'created_by': self.context['request'].user,
            'lecture': Class.objects.get(id=self.context['lecture_id']),
            'is_announcement': False,
        }

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_by', 'created_at', 'comment_count', 'hits']
