from rest_framework import serializers
from .models import *
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'student_id', 'is_professor']
        ref_name = 'user-simple'


class ClassSerializer(serializers.ModelSerializer):
    student = UserSerializer(many=True)

    class Meta:
        model = Class
        fields = ['id', 'name']
