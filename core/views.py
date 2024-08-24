from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "core/home.html", {})

def signin(request):
    return render(request, "core/signin.html", {})

def signup(request):
    return render(request, "core/signup.html", {})


