from rest_framework import serializers
from etl.models import *


class ModuleContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleContent
        fields = ['file']


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
