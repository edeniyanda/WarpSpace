from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from warperprofile.models import Profile


def home(request):
    return render(request, "core/home.html", {})

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect("home_page")
        messages.info(request, "Invalid Username or Password")
        return redirect("signin_page")
    return render(request, "core/signin.html", {})

def signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmpassword = request.POST["password_confirm"]

        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect("signup_page")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken")
                return redirect("signup_page")
            else:
                user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,  password=confirmpassword)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                return redirect("home_page")
        else:
            messages.info(request, "Password doesn't Match")
            return redirect("signup_page")
    else:
        return render(request, "core/signup.html", {})

def profilepage(request):
    pass
