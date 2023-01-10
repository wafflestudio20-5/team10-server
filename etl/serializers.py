from rest_framework import serializers
from .models import *
from authentication.models import User


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'student_id', 'is_professor']


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name']


class EnrollDropSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(required=True, write_only=True)
    classes = ClassSerializer(many=True)

    class Meta:
        model = User
        fields = ['class_id', 'classes']
