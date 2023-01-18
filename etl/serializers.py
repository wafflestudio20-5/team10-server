from rest_framework import serializers
from .models import *
from authentication.models import User


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'student_id', 'is_professor']


class ClassSerializer(serializers.ModelSerializer):
    class ProfessorSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['username']

    created_by = ProfessorSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Class
        fields = ['id', 'name', 'created_by']


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
        fields = ['id', 'lecture', 'name', 'due_date', 'max_grade', 'weight', 'file']


class AssignmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'lecture', 'created_by', 'name', 'due_date', 'max_grade', 'weight', 'file']


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
            Grade_info.is_graded=True
            Grade_info.score=validated_data['score']
            Grade_info.save()
        except:
            raise serializers.ValidationError(
                'Invalid student'
            )
        return instance

    class Meta:
        model = Assignment
        fields = ['id', 'user_id', 'score']


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {
            **internal_value,
            'created_by': self.context['request'].user,
            'post': Post.objects.get(id=self.context['post_id']),
        }

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_by', 'created_at']


class CommentDetailSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_by', 'created_at']


# TODO: comment_count 추가된 것 확인, 동작 확인.
class PostSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)
    comment_count = serializers.IntegerField(
        source='comment.count',
        read_only=True,
    )

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {
            **internal_value,
            'created_by': self.context['request'].user,
            'lecture': Class.objects.get(id=self.context['lecture_id']),
            'is_announcement': True
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['content'] = instance.content[:10]
        return rep

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_by', 'created_at', 'comment_count']


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)
    comment = CommentSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_by'] = instance.created_by.username
        return rep

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_by', 'created_at', 'comment']


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'created_by', 'created_at', 'content']

    def create(self, validated_data):
        post = Post.objects.create(title=validated_data['title'], created_by=validated_data['created_by'], created_at=validated_data['created_at'], is_announcement=True)
        post.save()
        return post


class AssignmentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentToStudent
        fields = ['id', 'file']
