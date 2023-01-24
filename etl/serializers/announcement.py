from rest_framework import serializers
from etl.models import *


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'created_by', 'created_at', 'content']

    def create(self, validated_data):
        post = Post.objects.create(title=validated_data['title'], created_by=validated_data['created_by'], created_at=validated_data['created_at'], is_announcement=True)
        post.save()
        return post
