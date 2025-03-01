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

from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("enter/", views.enter),
    path("leave/", views.leave),
    path("register/", views.register),

    path("questions/", views.questions),
    path("questions/<int:question_id>", views.one_question),
    path("questions/<int:question_id>/answer/", views.answer),
    path("questions/my-questions/", views.my_questions),
    path("questions/my-questions/<int:question_id>/delete/", views.my_question_delete),
    path("questions/my-questions/<int:question_id>/edit/", views.edit_question),
    path("questions/favorites/", views.favorites_list_question),
    path("questions/favorites/<int:question_id>", views.favorite_question),
    path("questions/upvote/<int:question_id>", views.upvote_question),

    path("answer/<int:answer_id>/", views.answer_text),
    path("answer/<int:answer_id>/delete/", views.my_answer_delete),
    path("answer/<int:answer_id>/edit/", views.edit_answer),

    path("articles/", views.articles),
    path("articles/<int:article_id>", views.one_article),
    path("articles/<int:article_id>/comment/", views.comment),
    path("articles/my-articles/", views.my_articles),
    path("articles/my-articles/<int:article_id>/delete/", views.my_article_delete),
    path("articles/my-articles/<int:article_id>/edit/", views.edit_article),
    path("articles/favorites/", views.favorites_list_article),
    path("articles/favorites/<int:article_id>", views.favorite_article),
    path("articles/upvote/<int:article_id>", views.upvote_article),

    path("comment/<int:comment_id>/delete/", views.my_comment_delete),
    path("comment/<int:comment_id>/edit/", views.edit_comment),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
