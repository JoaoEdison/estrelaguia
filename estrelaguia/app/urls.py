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
    path("questions/my-questions/<int:question_id>/edit/", views.edit_question)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
