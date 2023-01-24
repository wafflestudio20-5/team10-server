from rest_framework import serializers
from etl.models import *


class ClassSerializer(serializers.ModelSerializer):
    class ProfessorSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['username']

    created_by = ProfessorSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    def create(self, validated_data):
        instance = super().create(validated_data)
        Module.objects.create(lecture=instance)
        return instance

    class Meta:
        model = Class
        fields = ['id', 'name', 'created_by']


class EnrollDropSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(required=True, write_only=True)
    classes = ClassSerializer(many=True)

    class Meta:
        model = User
        fields = ['class_id', 'classes']
