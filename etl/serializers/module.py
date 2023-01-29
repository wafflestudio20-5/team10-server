from rest_framework import serializers
from etl.models import *
import boto3, os

class ModuleContentSerializer(serializers.ModelSerializer):
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
        model = ModuleContent
        fields = ['url']


class ModuleContentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleContent
        fields = ['weekly', 'file']


class WeeklySerializer(serializers.ModelSerializer):
    module_content = ModuleContentSerializer(many=True, read_only=True)

    class Meta:
        model = Weekly
        fields = ['id', 'name', 'module_content']


class WeeklyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weekly
        fields = ['id', 'module', 'name']


class ModuleSerializer(serializers.ModelSerializer):
    weekly = WeeklySerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['lecture', 'weekly']
