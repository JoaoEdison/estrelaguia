#   Copyright 2025 João E. R. Manica
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

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
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=256, blank=True)
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
    name = models.CharField(max_length=256)
    ext = models.CharField(max_length=8)
    position = models.IntegerField(null=True)
    centralization = models.CharField(max_length=1, null=True)
    height = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)

class ArticleUpvote(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=['article', 'user'], name='unique_article_user_upvote'
                )
            ]
class CommentUpvote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=['comment', 'user'], name='unique_comment_user_upvote'
                )
            ]
class QuestionUpvote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=['question', 'user'], name='unique_question_user_upvote'
                )
            ]
class AnswerUpvote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=['answer', 'user'], name='unique_answer_user_upvote'
                )
            ]

class ArticleFavorite(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class QuestionFavorite(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
