from rest_framework import serializers
from etl.serializers import ClassSerializer
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
import re


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True, write_only=True)
    username = serializers.CharField(read_only=True)
    student_id = serializers.CharField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_professor = serializers.BooleanField(read_only=True)
    classes = ClassSerializer(many=True, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not regex.match(email):
            raise serializers.ValidationError("Invalid email format")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if not user.check_password(password):
                raise serializers.ValidationError('Wrong password')

        else:
            raise serializers.ValidationError("User does not exist")

        update_last_login(None, user)
        token = RefreshToken.for_user(user=user)

        data = {
            'user_id': user.id,
            'refresh_token': str(token),
            'access_token': str(token.access_token)
        }

        return data

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'student_id', 'is_professor', 'is_superuser', 'classes']


class UserDetailSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True, read_only=True)

    def validate_student_id(self, value: str):
        if len(value) != 10:
            raise serializers.ValidationError('student_id should be 10 length')
        if value[4] != '-':
            raise serializers.ValidationError('student_id form should be XXXX-XXXXX')
        try:
            user = User.objects.get(student_id=value)
            if user != self.context['request'].user:
                raise serializers.ValidationError('already existing student_id')
        except User.DoesNotExist:
            pass
        return value

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'student_id', 'profile', 'is_professor', 'is_superuser', 'classes', 'is_social_login']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    student_id = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    is_professor = serializers.BooleanField(required=True)

    def validate_student_id(self, value: str):
        if len(value) != 10:
            raise serializers.ValidationError('student_id should be 10 length')
        if value[4] != '-':
            raise serializers.ValidationError('student_id form should be XXXX-XXXXX')
        try:
            User.objects.get(student_id=value)
            raise serializers.ValidationError('already existing student_id')
        except User.DoesNotExist:
            pass
        return value

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['password'])
        user.username = validated_data['username']
        user.student_id = validated_data['student_id']
        user.is_professor = validated_data['is_professor']
        token = RefreshToken.for_user(user)
        user.refreshtoken = token
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'student_id', 'is_professor']


class UserIDSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['email']


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'new_password']

