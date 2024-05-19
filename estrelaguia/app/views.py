from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def index(req):
    template = loader.get_template("index.html")
    context = {}
    return HttpResponse(template.render(context, req))
