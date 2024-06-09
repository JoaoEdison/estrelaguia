from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template import loader
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, is_password_usable
from django.urls import reverse
from django.db.models import Q
from .models import *
import logging
from .utils import bread

logger = logging.getLogger(__name__)

class LoginForm(forms.Form):
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)
class RegisterForm(LoginForm):
    second_password = forms.CharField(label='Digite a senha novamente', widget=forms.PasswordInput)
    nome = forms.CharField()
    field_order = ['email', 'nome']

def index(req):
    template = loader.get_template("index.html")
    context = { 'question_list' :  Question.objects.order_by('-date')[:10] }
    return HttpResponse(template.render(context, req))

def enter(req):
    form = LoginForm()
    if req.method == 'POST':
        user = authenticate(req, email=req.POST['email'], password=req.POST['senha'])
        if user is None:
            return render(req, 'enter.html', {'form': form, 'error': "Usuário ou senha incorretos."})
        login(req, user)
        return HttpResponseRedirect(reverse('index'))
    return render(req, 'enter.html', { 'form': form, 'page_name' : 'Entrar' })

def leave(req):
    logout(req)
    return HttpResponseRedirect(reverse('index'))

def register(req):
    page = "register.html"
    context = { 'form' : RegisterForm(), 'page_name' : 'Cadastro' }

    if req.method == 'POST':
        name_field = req.POST['nome']
        email_field = req.POST['email']
        password_field = req.POST['senha']

        if password_field != req.POST['second_password']:
            context['error'] = "As senhas são diferentes."
            return render(req, page, context)
        try:
            user = EmailUser.objects.get(email=email_field)
        except EmailUser.DoesNotExist:
            try:
                user = EmailUser.objects.get(username=name_field)
            except EmailUser.DoesNotExist:
                password = make_password(password_field)
                if is_password_usable(password) == False:
                    context['error'] = "A senha é inválida."
                    return render(req, page, context)
                user = EmailUser(username=name_field, email=email_field, password=password)
                user.save()
            else:
                context['error'] = "Usuário já existe."
                return render(req, page, context)
        else:
            context['error'] = "Email já cadastrado."
            return render(req, page, context)
    return render(req, page, context)

def save_files(req, answer=None, article=None, question=None):
   items = req.FILES.getlist('files')
   for f in items:
       fname = f.name
       fields = req.POST.getlist(fname+'[]')
       dot = fname.find('.')
       fext = fname[dot:] 
       fname = fname[:dot]
       attach = Attachment(
           data = f,
           name = fname,
           ext = fext,
           position = fields[0],
           width = fields[1],
           height = fields[2],
           centralization = fields[3],
           answer = answer,
           article = article,
           question = question
       )
       attach.save()

def questions(req):
    if req.method == 'POST' and req.user.is_authenticated:
        new_question = Question.objects.create(text=req.POST['question_text'],
                                               user=req.user)
        new_question.save()
        save_files(req, question=new_question)
    if req.GET.get('my') == None:
        question_list = Question.objects.order_by('-date')
    else:
        question_list = Question.objects.filter(user=req.user.id).order_by('-date')
    pattern = req.GET.get('pattern')
    if pattern != None and pattern != '':
        question_list = question_list.filter(text__icontains=pattern)
    context = {
        'question_list' : question_list,
        'page_name' : 'Perguntas',
        'previous_pages' : bread(req.path)
    }
    return render(req, 'questions.html', context)

def my_question_delete(req, question_id):
    question = Question.objects.get(pk=question_id)
    if question.user.id == req.user.id and Answer.objects.filter(question=question_id).count() == 0:
        question.delete()
    return redirect(my_questions)

def my_questions(req):
    question_list = Question.objects.filter(user=req.user.id).order_by('-date')
    context = {
        'question_list' : question_list,
        'previous_pages' : bread(req.path)
    }
    return render(req, 'my-questions.html', context)

def edit_question(req, question_id):
    if req.method == 'POST' and req.user.is_authenticated:
        question = Question.objects.get(pk=question_id)
        question.text = req.POST['question_text']
        question.save()
        # Se eh um arranjo
        for i in req.POST.lists():
            field_name = i[0]
            parentesis = field_name.find("[]")
            if parentesis > -1:
                values = i[1]
                attach = Attachment.objects.filter(name=field_name[:parentesis])
                if attach:
                    if 'on' in values:                    
                        attach.delete()
                    else:
                        attach.update(
                            position = values[0],              
                            height = values[1],
                            width = values[2],
                            centralization = values[3]
                        )
        save_files(req, question=question)
        return redirect(my_questions)
    previous = bread(req.path)
    previous.pop(-2)
    context = {
        'question' : Question.objects.get(pk=question_id),
        'files' : Attachment.objects.filter(question=question_id),
        'previous_pages' : previous
    }
    return render(req, 'edit-question.html', context)

def include_imgs(objs, text):
    offset = 0
    for i in objs.all():
        img_tag = f"<img width=\"{i.width}\" height=\"{i.height}\" src=\"{i.data.url}\" />"
        text = text[:i.position+offset] + img_tag + text[i.position+offset:]
        offset += len(img_tag)
    return text

def one_question(req, question_id):
    question = Question.objects.get(pk=question_id)
    answers = Answer.objects.filter(question=question_id).order_by('date')
    changes = []
    for a in answers.all():
        a.text = include_imgs(Attachment.objects.filter(answer=a.id), a.text)
        changes.append(a)
    context = {
        'text' : include_imgs(Attachment.objects.filter(question=question_id), question.text),
        'question_id' : question_id,
        'likes' : QuestionUpvote.objects.filter(question=question_id).count(),
        'upvote' : QuestionUpvote.objects.filter(question=question_id, user=req.user.id).count() > 0,
        'favorite' : QuestionFavorite.objects.filter(question=question_id, user=req.user.id).count() > 0,
        'resp_list' : changes,
        'previous_pages' : bread(req.path)
    }
    return render(req, 'one-question.html', context)

def answer(req, question_id):
    if req.method == 'POST' and req.user.is_authenticated:
        new_answer = Answer.objects.create(text=req.POST['answer_text'],
                                           question=Question.objects.get(pk=question_id),
                                           user=req.user)
        new_answer.save()
        items = req.FILES.getlist('files')
        for f in items:
            fname = f.name
            fields = req.POST.getlist(fname+'[]')
            dot = fname.find('.')
            fext = fname[dot:] 
            fname = fname[:dot]
            attach = Attachment(
                data = f,
                name = fname,
                ext = fext,
                position = fields[0],
                width = fields[1],
                height = fields[2],
                centralization = fields[3],
                answer = new_answer
            )
            attach.save()
        return HttpResponseRedirect(req.POST['prev'])
    return HttpResponseNotFound("Recurso não encontrado.")

def articles(req):
    if req.method == 'POST' and req.user.is_authenticated:
        new_article = Article.objects.create(
                                            title    = req.POST['title'],
                                            subtitle = req.POST['subtitle'],
                                            text     = req.POST['article_text'],
                                            user     = req.user)
        new_article.save()
        save_files(req, article=new_article)

    if req.GET.get('my'):
        article_list = Article.objects.filter(user=req.user.id)
    else:
        article_list = Article.objects
    pattern = req.GET.get('pattern')
    if pattern != None and pattern != '':
        query = Q()
        if req.GET.get('title'):
            query = query | Q(title__icontains=pattern)
        if req.GET.get('subtitle'):
            query = query | Q(subtitle__icontains=pattern)
        if req.GET.get('text'):
            query = query | Q(text__icontains=pattern)
        article_list = article_list.filter(query)
    context = {
        'article_list' : article_list.order_by('-date'),
        'page_name' : 'Artigos',
        'previous_pages' : bread(req.path)
    }
    return render(req, 'articles.html', context)

def one_article(req, article_id):
    article = Article.objects.get(pk=article_id)
    comments = Comment.objects.filter(article=article_id).order_by('date')
    context = {
        'text' : include_imgs(Attachment.objects.filter(article=article_id), article.text),
        'article' : article,
        'likes' : ArticleUpvote.objects.filter(article=article_id).count(),
        'upvote' : ArticleUpvote.objects.filter(article=article_id, user=req.user.id).count() > 0,
        'favorite' : ArticleFavorite.objects.filter(article=article_id, user=req.user.id).count() > 0,
        'comment_list' : comments,
        'previous_pages' : bread(req.path)
    }
    return render(req, 'one-article.html', context)

def comment(req, article_id):
    if req.method == 'POST' and req.user.is_authenticated:
        new_comment = Comment.objects.create(text=req.POST['comment_text'],
                                           article=Article.objects.get(pk=article_id),
                                           user=req.user)
        new_comment.save()
        return HttpResponseRedirect(req.POST['prev'])
    return HttpResponseNotFound("Recurso não encontrado.")

def my_article_delete(req, article_id):
    article = Article.objects.get(pk=article_id)
    if article.user.id == req.user.id and Comment.objects.filter(article=article_id).count() == 0:
        article.delete()
    return redirect(my_articles)

def my_articles(req):
    article_list = Article.objects.filter(user=req.user.id).order_by('-date')
    context = {
        'article_list' : article_list,
        'previous_pages' : bread(req.path)
    }
    return render(req, 'my-articles.html', context)

def edit_article(req, article_id):
    if req.method == 'POST' and req.user.is_authenticated:
        article = Article.objects.get(pk=article_id)
        article.title = req.POST['title']
        article.subtitle = req.POST['subtitle']
        article.text = req.POST['article_text']
        article.save()
        for i in req.POST.lists():
            field_name = i[0]
            parentesis = field_name.find("[]")
            if parentesis > -1:
                values = i[1]
                attach = Attachment.objects.filter(name=field_name[:parentesis])
                if attach:
                    if 'on' in values:
                        attach.delete()
                    else:
                        attach.update(
                            position = values[0],              
                            height = values[1],
                            width = values[2],
                            centralization = values[3]
                        )
        save_files(req, article=article)
        return redirect(my_articles)
    previous = bread(req.path)
    previous.pop(-2)
    context = {
        'article' : Article.objects.get(pk=article_id),
        'files' : Attachment.objects.filter(article=article_id),
        'previous_pages' : previous
    }
    return render(req, 'edit-article.html', context)

def my_comment_delete(req, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if comment.user.id == req.user.id and req.user.is_authenticated:
        comment.delete()
    return HttpResponse('')

def edit_comment(req, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if comment.user.id == req.user.id and req.user.is_authenticated:
        comment.text = req.body.decode('utf-8')
        comment.save()
    return HttpResponse('')

def upvote_article(req, article_id):
    if req.method == 'POST':
        upvote = ArticleUpvote.objects.create(article = Article.objects.get(pk=article_id),
                                              user    = req.user)
        upvote.save()
    elif req.method == 'DELETE':
        upvote = ArticleUpvote.objects.filter(article = article_id, user = req.user)
        upvote.delete()
    return HttpResponse('')
def upvote_question(req, question_id):
    if req.method == 'POST':
        upvote = QuestionUpvote.objects.create(question = Question.objects.get(pk=question_id),
                                               user    = req.user)
        upvote.save()
    elif req.method == 'DELETE':
        upvote = QuestionUpvote.objects.filter(question = question_id, user = req.user)
        upvote.delete()
    return HttpResponse('')

def favorite_article(req, article_id):
    if req.method == 'POST':
        favorite = ArticleFavorite.objects.create(article = Article.objects.get(pk=article_id),
                                                  user    = req.user)
        favorite.save()
    elif req.method == 'DELETE':
        favorite = ArticleFavorite.objects.filter(article = article_id, user = req.user)
        favorite.delete()
    return HttpResponse('')
def favorite_question(req, question_id):
    if req.method == 'POST':
        favorite = QuestionFavorite.objects.create(question = Question.objects.get(pk=question_id),
                                                   user    = req.user)
        favorite.save()
    elif req.method == 'DELETE':
        favorite = QuestionFavorite.objects.filter(question = question_id, user = req.user)
        favorite.delete()
    return HttpResponse('')

def favorites_list_article(req):
    context = {
        'fav_list' : ArticleFavorite.objects.filter(user = req.user).select_related('article').order_by('-id'),
        'previous_pages' : bread(req.path)
    }
    return render(req, 'fav-articles.html', context)
def favorites_list_question(req):
    context = {
        'fav_list' : QuestionFavorite.objects.filter(user = req.user).select_related('question').order_by('-id'),
        'previous_pages' : bread(req.path)
    }
    return render(req, 'fav-questions.html', context)
