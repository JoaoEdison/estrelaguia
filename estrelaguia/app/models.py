from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class EmailUser(AbstractUser):
    email = models.EmailField(unique=True)

User = get_user_model()

class Question(models.Model):
    text = models.CharField()
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Answer(models.Model):
    text = models.CharField()
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Article(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=60, blank=True)
    text = models.CharField()
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Comment(models.Model):
    text = models.CharField()
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

class Attachment(models.Model):
    data = models.FileField()
    name = models.CharField(max_length=100)
    ext = models.CharField(max_length=8)
    position = models.IntegerField(null=True)
    centralization = models.CharField(max_length=1, null=True)
    height = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
