from django.shortcuts import render
from django.http import  HttpResponse

def index(request):
    return  HttpResponse('Hello World')

def about(request):
    return HttpResponse('Page for me')

