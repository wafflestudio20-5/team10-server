from django.db import models
from authentication.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Class(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # related_name을 정의하면, User.classes 를 통해서 특정 유저가 수강하는 강의에 접근 가능
    # 자세한 내용은 https://velog.io/@jiffydev/Django-9.-ManyToManyField-1 참고
    student = models.ManyToManyField(User, related_name='classes')


class Assignment(models.Model):
    lecture = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    due_date = models.DateTimeField()
    max_grade = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],)
    student = models.ManyToManyField(User, related_name='assignments', through="AssignmentToStudent")
    file = models.FileField(null=True, upload_to="assignments/", blank=True)


class Post(models.Model):
    lecture = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)
    is_announcement = models.BooleanField(default=False)
    hits = models.IntegerField(default=0)


class Comment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)


class AssignmentToStudent(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    is_submitted = models.BooleanField(default=False)
    is_graded = models.BooleanField(default=False)
    score = models.FloatField(default=0)
    file = models.FileField(null=True, upload_to="submissions/", blank=True)

class Module(models.Model):
    lecture = models.OneToOneField(Class, on_delete=models.CASCADE, related_name='module')

class Weekly(models.Model):
    name = models.CharField(max_length=50, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='weekly')

class ModuleContent(models.Model):
    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE, related_name='module_content')
    file = models.FileField(null=True, upload_to="modules/", blank=True)