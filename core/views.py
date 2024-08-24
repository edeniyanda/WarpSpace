from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("This is the home pasge")

def signin(request):
    return HttpResponse("This is the sign in pasge")

def signup(request):
    return HttpResponse("This is the signup pasge")


