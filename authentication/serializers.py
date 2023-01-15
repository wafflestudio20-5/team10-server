from rest_framework import serializers
from etl.serializers import ClassSerializer
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True, write_only=True)
    username = serializers.CharField(read_only=True)
    student_id = serializers.CharField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_professor = serializers.BooleanField(read_only=True)
    classes = ClassSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep['token'] = instance.auth_token.key
        except:
            rep['token'] = 'no token. please contact developers'
        return rep

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'student_id', 'is_professor', 'is_superuser', 'classes']


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
    student_id = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

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
