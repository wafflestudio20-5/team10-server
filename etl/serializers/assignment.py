from rest_framework import serializers
from etl.models import *
import boto3, os


class AssignmentCreateSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    def create(self, validated_data):
        assignment = super().create(validated_data)
        lecture = validated_data['lecture']
        for s in lecture.student.all():
            assignment.student.add(s)
        assignment.save()
        return assignment

    class Meta:
        model = Assignment
        fields = ['id', 'lecture', 'name', 'category', 'due_date', 'max_grade', 'weight', 'file']


class AssignmentDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    def get_url(self, obj):
        path =  obj.file.name
        if path=='':
            return 'null'
        s3 = boto3.client('s3', region_name=os.environ.get('AWS_REGION'),
                          aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        link = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'etl-media-database',
                'Key': path,
            },
            ExpiresIn=600
        )
        return link
    class Meta:
        model = Assignment
        fields = ['id', 'lecture', 'created_by', 'name', 'category', 'due_date', 'max_grade', 'weight', 'file', 'url']


class AssignmentToStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentToStudent
        fields = ['id', 'is_submitted', 'is_graded', 'score']


class AssignmentGradingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    score = serializers.FloatField(write_only=True)

    def update(self, instance, validated_data):
        try:
            student = User.objects.get(id=validated_data['user_id'])
            Grade_info = AssignmentToStudent.objects.get(student=student, assignment=instance)
            Grade_info.is_graded = True
            Grade_info.score = validated_data['score']
            Grade_info.save()
        except:
            raise serializers.ValidationError(
                'Invalid student'
            )
        return instance

    class Meta:
        model = Assignment
        fields = ['id', 'user_id', 'score']


class AssignmentFileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        path = obj.file.name
        if path == '':
            return 'null'
        s3 = boto3.client('s3', region_name=os.environ.get('AWS_REGION'),
                          aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        link = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'etl-media-database',
                'Key': path,
            },
            ExpiresIn=600
        )
        return link
    class Meta:
        model = AssignmentToStudent
        fields = ['id', 'url']