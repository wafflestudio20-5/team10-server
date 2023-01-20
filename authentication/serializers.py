from etl.serializers import ClassSerializer
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True, write_only=True, style={'input_type': 'password'})
    # classes = ClassSerializer(many=True)
    # token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'student_id', 'is_professor', 'is_superuser']

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     try:
    #         rep['token'] = instance.auth_token.key
    #     except:
    #         rep['token'] = 'no token. please contact developers'
    #     return rep

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if not user.check_password(password):
                raise serializers.ValidationError('Check Your Email or Password')

        else:
            raise serializers.ValidationError("User does not exist")

        update_last_login(None, user)
        token = RefreshToken.for_user(user=user)

        data = {
            'user': user.id,
            'refresh_token': str(token),
            'access_token': str(token.access_token)
        }

        return data


class UserDetailSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep['token'] = instance.auth_token.key
        except:
            rep['token'] = 'no token. please contact developers'
        return rep

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'student_id', 'is_professor', 'is_superuser', 'classes']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'}, validators=[validate_password])
    is_professor = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'student_id', 'is_professor']

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['password'])
        user.username = validated_data['username']
        user.student_id = validated_data['student_id']
        user.is_professor = validated_data['is_professor']
        token = RefreshToken.for_user(user)
        user.refreshtoken = token
        user.save()
        return user


class UserIDSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['email']
