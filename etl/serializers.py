from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PostListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    # user_info = UserSerializer(source='created_by', read_only=True)

    # POST 내용은 List 요청 시 최대 앞 300자만 보낸다
    # to_representation 메서드에서 description 을 300자로 자르는 것이 좋은가
    # 혹은 views.py 에서 get 함수 자체에서 description 을 300자로 잘라 보내는 것이 좋은가
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['description'] = instance.description[:300]
        representation['created_by'] = instance.created_by.username
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at']
