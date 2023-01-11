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
        fields = ['id', 'lecture', 'name', 'due_date', 'max_grade', 'weight']


class AssignmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'lecture', 'created_by', 'name', 'due_date', 'max_grade', 'weight']


class AssignmentToStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentToStudent
        fields = ['id', 'is_submitted', 'is_graded', 'score']


class AssignmentGradingSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(max_length=10, write_only=True)
    score = serializers.FloatField(write_only=True)

    def update(self, instance, validated_data):
        try:
            student = User.objects.get(student_id=validated_data['student_id'])
            Grade_info = AssignmentToStudent.objects.get(student=student, assignment=instance)
            Grade_info.is_graded=True
            Grade_info.score=validated_data['score']
            Grade_info.save()
        except:
            raise serializers.ValidationError(
                'Invalid student id'
            )
        return instance

    class Meta:
        model = Assignment
        fields = ['id', 'student_id', 'score']
