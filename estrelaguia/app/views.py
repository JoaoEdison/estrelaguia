from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.template import loader
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, is_password_usable
from django.urls import reverse
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

def questions(req):
    if req.method == 'POST' and req.user.is_authenticated:
        new_question = Question.objects.create(text=req.POST['question_text'],
                                               user=req.user)
        new_question.save()
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
                question = new_question
            )
            attach.save()
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

def my_questions(req):
    question_list = Question.objects.filter(user=req.user.id).order_by('-date')
    context = {
        'question_list' : question_list,
        'previous_pages' : bread(req.path)
    }
    return render(req, 'my-questions.html', context)

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
        'resp_list' : changes,
        'previous_pages' : bread(req.path)
    }
    return render(req, 'one_question.html', context)

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
