from django.db import models
from authentication.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Class(models.Model):
    name = models.CharField(max_length=50)
    student = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)


class Announcement(models.Model):
    lecture = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(null=True, blank=True)
    is_announcement = models.BooleanField(default=True)


class Assignment(models.Model):
    lecture = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    due_date = models.DateTimeField()
    max_grade = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],)


class Post(models.Model):
    lecture = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(null=True, blank=True)
    is_announcement = models.BooleanField(default=False)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(null=True, blank=True)
