from rest_framework import serializers
from etl.models import *
from .user import UserSimpleSerializer
from .comment import CommentSerializer


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)
    comment = CommentSerializer(many=True, read_only=True)
    hits = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_by', 'created_at', 'comment', 'hits']


class PostSimpleSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)
    comment_count = serializers.IntegerField(
        source='comment.count',
        read_only=True,
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_by', 'created_at', 'comment_count']
